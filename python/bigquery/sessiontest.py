from google.cloud import bigquery
import sys


def read_query_from_file(file_path):
    """Reads the query string from a specified file."""
    with open(file_path, "r") as file:
        return file.read()


# Retrieve the path to the SQL file from command-line arguments
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
# job_config = bigquery.QueryJobConfig(destination=table_ref, write_disposition=write_disposition, create_session=True)
job_config = bigquery.QueryJobConfig(create_session=True)
query_job = client.query(query, job_config=job_config)

results = query_job.result()
print(query_job.session_info.session_id)
# target_table_ref = bigquery.TableReference("gke-expeiments", "curated_zone", "test")
table_id = "gke-expeiments.curated_zone.test"
print("creating job config")
write_job_config = bigquery.QueryJobConfig(
    create_session=False,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    destination=table_id,
    connection_properties=[
        bigquery.query.ConnectionProperty(
            key="session_id", value=query_job.session_info.session_id
        )
    ]
)
print("running write query")
print(f"select * from ", "src")
write_query_job = client.query('SELECT * FROM src', job_config=write_job_config, location='us-central1')

