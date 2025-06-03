import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import time
import random


class GenerateData(beam.DoFn):
    def process(self, element):
        # Simulating the streaming data by yielding elements with a delay
        for i in range(10):
            yield {'msg_id': i, 'periodReference': random.randint(1, 5), "eventTimestamp": time.time()}
            time.sleep(1)


def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True
    options.view_as(StandardOptions).runner = 'DirectRunner'

    with beam.Pipeline(options=options) as p:
        data = (
            p
            | 'Create' >> beam.Create([None])
            | 'Generate Data' >> beam.ParDo(GenerateData())
            | "Window" >> beam.WindowInto(beam.window.FixedWindows(3))
        )

        sample_transformation = (
            data
            | "Sample " >> beam.Map(lambda x: {**x, "msg_id": x["msg_id"] ** 2})
        )

        # (
        #     data
        #     | 'Print' >> beam.Map(print)
        # )
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

        data_kv = data | "Key periodReference" >> beam.Map(lambda x: (x['periodReference'], x))
        sample_kv = sample_transformation | "Key Sampled Data" >> beam.Map(lambda x: (x['periodReference'], x))

        grouped_data = (
            {"data": data_kv, "sampled_data": sample_kv}
            | "CoGroupBy" >> beam.CoGroupByKey()
            | "Print" >> beam.Map(print)
        )


if __name__ == '__main__':
    run()
