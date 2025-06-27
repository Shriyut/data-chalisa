import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json

class PrintSideInputDoFn(beam.DoFn):
    def process(self, element, side_input):
        print(f"Side input content: {side_input} of type {type(side_input)}") # side input is passed as a dictionary
        # json_side_input = json.dumps(side_input)
        # print(f"JSON side input content: {json_side_input} of type {type(json_side_input)}") # treated as string
        print("Hogan params are :", side_input.get("hogan_parameters"))
        print("Column family mapping is :", side_input.get("column_family_mapping"))
        yield element  # or just `yield` if you don't need to output anything


def run():
    input_json_path = (r'C:\Users\shrijha\PycharmProjects\data-chalisa\apache_beam\python_sdk\direct_runner\data'
                       r'\sample.json')

    options = PipelineOptions([
        '--runner=DirectRunner'
    ])

    with beam.Pipeline(options=options) as p:
        # Read the entire file as a single string
        side_input_content = (
            p
            | 'Create file path' >> beam.Create([input_json_path])
            | 'Read file' >> beam.Map(lambda path: open(path).read())
            | 'Parse JSON' >> beam.Map(json.loads)
        )

        main_input = p | 'Main input' >> beam.Create([None])

        _ = (
            main_input
            | 'Print side input' >> beam.ParDo(
                PrintSideInputDoFn(),
                side_input=beam.pvalue.AsSingleton(side_input_content)
            )
        )


if __name__ == '__main__':
    run()
