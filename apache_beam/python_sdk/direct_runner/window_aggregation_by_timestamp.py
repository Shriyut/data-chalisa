import apache_beam as beam
from apache_beam import PTransform
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import time
import datetime
import random
import logging


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
                    "eventTimestamp": now.strftime('%Y%m%d%H%M%S%f')
                }, now.timestamp()
            )
            time.sleep(1)


class AssignWindowId(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        window_start_time = window.start.to_utc_datetime()
        window_id = window_start_time.strftime('%Y%m%d%H%M%S')
        yield window_id, element


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

        # sample_transformation = (
        #         data
        #         | "Sample " >> beam.Map(lambda x: {**x, "msg_id": x["msg_id"] ** 2})
        # )

        (
                grouped_data
                | 'Print' >> beam.Map(print)
        )
        #
        # (
        #     sample_transformation
        #     | 'Print Sampled Data' >> beam.Map(print)
        # )

        # aggregated_data = (
        #     (
        #         {
        #             "input_data": data, "processed_data": sample_transformation
        #         }
        #     )
        #     | 'Merge Data' >> beam.CoGroupByKey()
        #     | 'Process Merged Data' >> beam.Map(print)
        # )

        # data_kv = data | "Key periodReference" >> beam.Map(lambda x: (x['periodReference'], x))
        # sample_kv = sample_transformation | "Key Sampled Data" >> beam.Map(lambda x: (x['periodReference'], x))
        #
        # grouped_data = (
        #         {"data": data_kv, "sampled_data": sample_kv}
        #         | "CoGroupBy" >> beam.CoGroupByKey()
        #         | "Print" >> beam.Map(print)
        # )


def log_events(element):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting the window aggregation process...")
    str_elem = str(element)
    logging.info(f"Processing element: {str_elem}")


if __name__ == '__main__':
    run()
