import apache_beam as beam
from apache_beam import PTransform
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import time
import datetime
import random
import logging
import json

from apache_beam.transforms.ptransform import InputT, OutputT


class GenerateData(beam.DoFn):
    def process(self, element, timestamp=beam.DoFn.TimestampParam):
        # unix_timestamp = extract_timestamp_from_log_entry(element)
        for i in range(10):
            # yield {'msg_id': i, 'periodReference': random.randint(1, 5),
            #        "eventTimestamp": datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}
            now = datetime.datetime.now()
            yield beam.window.TimestampedValue(
                {
                    'msg_id': i,
                    'periodReference': random.randint(1, 5),
                    'sample_value': random.randint(20, 22),
                    "sample_amount": random.randint(100, 200),
                    "eventTimestamp": now.strftime('%Y%m%d%H%M%S%f')
                }, now.timestamp()
            )
            time.sleep(1)


class AssignWindowId(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        window_start_time = window.start.to_utc_datetime()
        window_id = window_start_time.strftime('%Y%m%d%H%M%S')
        elem_new = json.loads(str(element).replace("'", '"'))
        elem_new['window_id'] = window_id
        yield elem_new


class GroupMessagesByWindow(PTransform):
    def expand(self, p_collection):
        return (
                p_collection
                | "Assign Window" >> beam.WindowInto(beam.window.FixedWindows(3))
                | "Assign Window ID" >> beam.ParDo(AssignWindowId())
            # | "Group by Window ID" >> beam.GroupByKey()
            # | "Format Output" >> beam.Map(lambda x: {'window_id': x[0], 'messages': list(x[1])})
        )


def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True
    options.view_as(StandardOptions).runner = 'DirectRunner'

    with beam.Pipeline(options=options) as p:
        # data = (
        #         p
        #         | 'Create' >> beam.Create([None])
        #         | 'Generate Data' >> beam.ParDo(GenerateData())
        #         | "Window" >> beam.WindowInto(beam.window.FixedWindows(3))
        # )

        data = (
                p
                | 'Create' >> beam.Create([None])
                | 'Generate Data' >> beam.ParDo(GenerateData())
        )

        grouped_data = (
                data
                | "Group Messages by Window" >> GroupMessagesByWindow()
        )

        # grouped_by_period_and_window = (
        #         grouped_data
        #         | "Key by periodReference and window_id" >> beam.Map(
        #     lambda x: ((x['periodReference'], x['window_id']), x)
        # )
        #         | "Group by key" >> beam.GroupByKey()
        #         # Optional: format output
        #         | "Format grouped output" >> beam.Map(
        #     lambda kv: {
        #         'periodReference': kv[0][0],
        #         'window_id': kv[0][1],
        #         'messages': list(kv[1])
        #     }
        # )
        # )

        (
                grouped_data
                | 'Print' >> beam.Map(print)
        )

        # after the pubsub msgs have been parsed and windowed with window_id,
        # they will be sent to the next step for further processing
        #  for audit at eeh level we will maintain the grouped records per window_id and periodReference
        eeh_records = grouped_data

        #eeh_records will be sent to the subsequent data processing dofns
        # audit metrics will be captured parallely

        # TODO: construct the EEH level audit log here

        eeh_audit_log = (
            eeh_records
            | "Eeh audit log" >> EehAuditAggregator()
            # | "Print1" >> beam.Map(print)
        )

        # TODO: construct EQH level audit log here

        transformed_records = eeh_records | "Filter and Multiply" >> beam.ParDo(ApplySampleTransformation())
        # removing all elements with sample_value that are prime numbers
        # (
        #     transformed_records | "print2" >> beam.Map(print)
        # )

        eqh_audit_log = (
            transformed_records
            | "Eqh audit log" >> EqhAuditAggregator()
            # | "Print3" >> beam.Map(print)
        )

        # TODO: Reconcile EEH & EQH audit logs here and build the tablerow for window_metadata

        merged_audit_log = (
            p
            | "Merge Audit Logs" >> MergeAuditLogs(eeh_audit_log, eqh_audit_log)
        )

        (
            merged_audit_log | "Print4" >> beam.Map(print)
        )

        # use output tags to highlight for errors and populate the failed transactions and transformation_issue_log here

        # sample_transformation = (
        #         data
        #         | "Sample " >> beam.Map(lambda x: {**x, "sample_value": x["sample_value"] ** 2})
        # )

        # (
        #         grouped_by_period_and_window
        #         | 'Print' >> beam.Map(print)
        # )


class MergeAuditLogs(PTransform):

    def __init__(self, eeh_pcol, eqh_pcol):
        self.eeh_pcol = eeh_pcol
        self.eqh_pcol = eqh_pcol

    def expand(self, pbegin):
        eeh = (
            self.eeh_pcol
            | "Filter EEH" >> beam.Filter(lambda x: x is not None)
            | "Keyed EEH audit log" >> beam.Map(lambda x: ((x['periodReference'], x['window_id']), x))
        )
        eqh = (
            self.eqh_pcol
            | "Filter EQH" >> beam.Filter(lambda x: x is not None)
            | "Keyed EQH audit log" >> beam.Map(lambda x: ((x['periodReference'], x['window_id']), x))
        )
        # return (
        #     {'eeh': eeh, 'eqh': eqh}
        #     | "CoGroupBy" >> beam.CoGroupByKey()
        #     | "Format to Tablerow" >> beam.Map(
        #         lambda kv: {
        #             'periodReference': kv[0][0],
        #             'window_id': kv[0][1],
        #             'eeh_audit': kv[1]['eeh'],
        #             'eqh_audit': kv[1]['eqh'],
        #         }
        #     )
        # )
        return (
            {'eeh': eeh, 'eqh': eqh}
            | "CoGroupBy" >> beam.CoGroupByKey()
            | "Format to Tablerow" >> beam.Map(self.flatten_audit_logs)
        )

    @staticmethod
    def flatten_audit_logs(kv):
        period_ref, window_id = kv[0]
        eeh = kv[1]['eeh'][0] if kv[1]['eeh'] else {}
        eqh = kv[1]['eqh'][0] if kv[1]['eqh'] else {}
        return {
            'periodReference': period_ref,
            'window_id': window_id,
            'count_at_eeh': eeh.get('count_at_eeh', 0),
            'total_amount_at_eeh': eeh.get('total_amount_at_eeh', 0),
            'eeh_audit_timestamp': eeh.get('eeh_audit_timestamp', datetime.datetime.now().isoformat()),
            'count_at_eqh': eqh.get('count_at_eqh', 0),
            'total_amount_at_eqh': eqh.get('total_amount_at_eqh', 0),
            'eqh_audit_timestamp': eqh.get('eqh_audit_timestamp', datetime.datetime.now().isoformat()),
        }


class EqhAuditAggregator(PTransform):
    def expand(self, p_collection):
        return (
            p_collection
            | "Tuple with periodRef and id" >> beam.Map(
                lambda x: ((x['periodReference'], x['window_id']), (1, x['sample_amount']))
            )
            | "Combine count and amount" >> beam.CombinePerKey(add_counts_and_amounts)
            | "Format output" >> beam.Map(
                lambda kv: {
                    'periodReference': kv[0][0],
                    'window_id': kv[0][1],
                    'count_at_eqh': kv[1][0],
                    'total_amount_at_eqh': kv[1][1],
                    'eqh_audit_timestamp': datetime.datetime.now().isoformat()
                }
            )
        )


class EehAuditAggregator(PTransform):
    def expand(self, p_collection):
        return (
            p_collection
            | "Tuple with periodRef and id" >> beam.Map(
                lambda x: ((x['periodReference'], x['window_id']), (1, x['sample_amount']))
            )
            | "Combine count and amount" >> beam.CombinePerKey(add_counts_and_amounts)
            | "Format output" >> beam.Map(
                lambda kv: {
                    'periodReference': kv[0][0],
                    'window_id': kv[0][1],
                    'count_at_eeh': kv[1][0],
                    'total_amount_at_eeh': kv[1][1],
                    'eeh_audit_timestamp': datetime.datetime.now().isoformat()
                }
            )
        )


class ApplySampleTransformation(beam.DoFn):
    # TODO: use side outputs to simulaate entries for failed_transactions and issue_log table
    def process(self, element):
        value = element.get('sample_value')
        if value is not None and is_prime(value):
            return
        # element['sample_value'] = value * 2
        yield element


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def log_events(element):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting the window aggregation process...")
    str_elem = str(element)
    logging.info(f"Processing element: {str_elem}")


def add_counts_and_amounts(values):
    count = 0
    total = 0
    for c, t in values:
        count += c
        total += t
    return count, total


if __name__ == '__main__':
    run()
