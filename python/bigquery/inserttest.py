from google.cloud import bigquery
import sys
import logging
from datetime import datetime


def read_query_from_file(file_path):
    """Reads the query string from a specified file."""
    with open(file_path, "r") as file:
        return file.read()


def insert_records():
    print("starting execution")
    query_file_path = sys.argv[1]

    client = bigquery.Client()
    location = "us-central1"

    # Read the query string from the provided file path
    query = read_query_from_file(query_file_path)

    # Access destination dataset and table from Argo workflow parameters
    destination_dataset = "curated_zone"
    destination_table = "test"
    # write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    table_ref = client.dataset(destination_dataset).table(destination_table)
    print("Start time: "+str(datetime.now()))
    table_id = "gke-expeiments.test.t1"
    print("creating job config")
    write_job_config = bigquery.QueryJobConfig(
        create_session=False,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
        destination=table_id,
        use_query_cache=False,
        # connection_properties=[
        #     bigquery.query.ConnectionProperty(
        #         key="session_id", value=query_job.session_info.session_id
        #     )
        # ],
        # query_parameters=[
        #     bigquery.ScalerQueryParameter("colName", "dataType", variable)
        # ]
    )
    write_query_job = client.query(query, job_config=write_job_config, location='us-central1')
    print("End time: "+str(datetime.now()))


insert_records()