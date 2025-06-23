import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, SetupOptions
import logging
from google.cloud import bigtable, bigquery
import json
import datetime
from google.cloud.bigtable import row
from google.cloud.bigtable.row import DirectRow


def log_events(element):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    str_elem = str(element)
    logger.info(f"Processing element: {str_elem} of type {type(element)}")


class CustomPipelineOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--patchingBqTableId',
            help='Bigquery table with patching details')
        parser.add_argument(
            '--projectId',
            help='GCP Project ID where BigTable is present')
        parser.add_argument(
            '--instanceId',
            help='BigTable Instance ID')
        parser.add_argument(
            '--lookupTableId',
            help='BigTable Table ID')
        parser.add_argument(
            '--patchingTableId',
            help='BigTable Table ID')
        parser.add_argument(
            '--hoganTableId',
            help='BigTable Table ID')
        parser.add_argument(
            '--hoganFieldMappingFilePath',
            help='BigTable Table ID')

        # cf - content: dinNumber  # product_code#serial_number#transactionId


class PatchTDSRecords(beam.DoFn):

    def __init__(self, pipeline_options, *unused_args, **unused_kwargs):
        # super().__init__(unused_args, unused_kwargs)
        self.hogan_table = None
        self.lookup_table = None
        self.table = None
        self.instance = None
        self.bigtable_client = None
        self.test = None
        self.pipeline_options = pipeline_options
        self.projectId = pipeline_options.get('projectId')
        self.instanceId = pipeline_options.get('instanceId')
        self.tableId = pipeline_options.get('patchingTableId')
        self.lookupTableId = pipeline_options.get('lookupTableId')
        self.hoganTableId = pipeline_options.get('hoganTableId')

    def setup(self):
        self.bigtable_client = bigtable.Client(project=self.projectId, admin=True)
        self.instance = self.bigtable_client.instance(self.instanceId)
        self.table = self.instance.table(self.tableId)
        self.lookup_table = self.instance.table(self.lookupTableId)
        self.hogan_table = self.instance.table(self.hoganTableId)

    def teardown(self):
        self.bigtable_client.close()

    def process(self, element, hogan_field_mapping_si):
        # from google.cloud.bigtable.row import DirectRow
        lookup_rowkey = element.get('tds_lookup_rowkey')
        element["lookup_rowkey"] = lookup_rowkey
        posting_date = str(element.get('posting_Date'))
        element["posting_Date"] = posting_date
        hogan_rowkey = element.get('tds_hogan_rowkey')
        hogan_fields = json.loads(hogan_field_mapping_si)
        try:
            lookup_row_data = self.lookup_table.read_row(lookup_rowkey)
            if lookup_row_data:

                logging.info(f"Row found for lookup table {lookup_rowkey}, updating posting date and status")

                # hogan_rowkey = lookup_row_data.cells['cf-rowkey'][b'hogan_rowkey'][0].value.decode('utf-8')
                tds_rowkey = lookup_row_data.cells['cf-rowkey'][b'tds_rowkey'][0].value.decode('utf-8')

                logging.info(f"Rowkeys read from lookup table: hogan_rowkey={hogan_rowkey}, tds_rowkey={tds_rowkey}")
                # read hogan fields from hogan table
                element['hogan_rowkey'] = hogan_rowkey
                element['tds_rowkey'] = tds_rowkey

                hogan_row_data = self.hogan_table.read_row(hogan_rowkey)
                tds_row_data = self.table.direct_row(tds_rowkey)
                logging.info(f"Row found for hogan table {hogan_rowkey} and {tds_row_data}, updating fields")

                if hogan_row_data and tds_row_data:
                    for cf, qualifiers in hogan_fields.items():
                        for qualifier in qualifiers:
                            cell = hogan_row_data.cells.get(cf, {}).get(qualifier.encode('utf-8'))
                            if cell and len(cell) > 0:
                                value = cell[0].value.decode('utf-8')
                                # element[f"{cf}:{qualifier}"] = value
                                element[f"{qualifier}"] = value
                            else:
                                logging.warning(f"No value found for {cf}:{qualifier} in hogan row {hogan_rowkey}")

                tds_row_data.set_cell('cf-transaction', 'postingDate', element.get("posting_Date").encode('utf-8'))
                tds_row_data.set_cell('cf-transaction', 'transactionStatus', 'PATCHED'.encode('utf-8'))
                tds_row_data.set_cell('cf-metadata', 'hogan_dinNumber', element.get("dinNumber").encode('utf-8'))
                tds_row_data.set_cell('cf-metadata', 'hogan_product_code', element.get("product_code").encode('utf-8'))
                tds_row_data.set_cell('cf-metadata', 'hogan_serial_number', element.get("serial_number").encode('utf-8'))
                tds_row_data.set_cell('cf-metadata', 'hogan_transactionId', element.get("transactionId").encode('utf-8'))
                tds_row_data.set_cell('cf-metadata', 'hogan_lastUpdateTimestamp', element.get("lastUpdateTimestamp").encode('utf-8'))
                tds_row_data.set_cell('cf-metadata', 'lastUpdateTimestamp', datetime.datetime.now().isoformat().encode('utf-8'))
                tds_row_data.commit()

                yield element
            else:
                logging.warning(f"No row found for key {lookup_rowkey}")
            # yield element
        except Exception as e:
            logging.exception(f"Error processing element {element}: {e}")


class UpdateBQTable(beam.DoFn):

    def __init__(self, pipeline_options):
        # super().__init__()
        self.projectId = pipeline_options.get('projectId')
        self.tableId = pipeline_options.get('patchingBqTableId')
        self.bq_client = None

    def setup(self):
        self.bq_client = bigquery.Client(project=self.projectId)

    def process(self, element, *args, **kwargs):

        lookup_rowkey = element.get('lookup_rowkey')
        if not lookup_rowkey:
            logging.info("Lookup rowkey not passed from patching step")

        query = f"""
            UPDATE `{self.tableId}`
            SET status = 'PATCHED',
                update_timestamp = CURRENT_TIMESTAMP()
            WHERE tds_lookup_rowkey = @lookup_rowkey
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("lookup_rowkey", "STRING", lookup_rowkey)
            ]
        )
        self.bq_client.query(query, job_config=job_config).result()
        yield element


def run(argv=None, save_main_session=True):

    pipeline_options = PipelineOptions()
    dataflow_options = pipeline_options.view_as(CustomPipelineOptions)
    pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'
    pipeline_options.view_as(StandardOptions).streaming = False
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
    pipeline_object = beam.Pipeline(options=pipeline_options)

    bq_table = dataflow_options.patchingBqTableId
    query = f"SELECT tds_lookup_rowkey, posting_Date, tds_hogan_rowkey FROM `{bq_table}` WHERE status = 'ACTIVE'"

    unmatched_records = (
            pipeline_object
            | "Read from BigQuery" >> beam.io.ReadFromBigQuery(query=query, use_standard_sql=True)
    )

    hogan_field_mapping_file = (
        pipeline_object | "Read from GCS" >> beam.io.ReadFromText(dataflow_options.hoganFieldMappingFilePath)
    )

    # (
    #     hogan_field_mapping_file
    #     | "Pring file" >> beam.Map(log_events)
    # )

    hogan_field_mapping_si = beam.pvalue.AsSingleton(hogan_field_mapping_file)

    patched_records = (
        unmatched_records
        | "Patch TDS Records" >> beam.ParDo(PatchTDSRecords(dataflow_options.get_all_options()), hogan_field_mapping_si)
        # | "Log Patched Records" >> beam.Map(log_events)
    )

    (
        patched_records
        | "map" >> beam.Map(log_events)
    )

    (
        patched_records
        | "Patch audit table" >> beam.ParDo(UpdateBQTable(dataflow_options.get_all_options()))
    )

    pipeline_object.run()


if __name__ == '__main__':
    run()
