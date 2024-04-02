from google.cloud import bigquery
import sys


def read_query_from_file(file_path):
    """Reads the query string from a specified file."""
    with open(file_path, "r") as file:
        return file.read()


# Retrieve the path to the SQL file from command-line arguments
query_file_path = sys.argv[1]

client = bigquery.Client()

# Read the query string from the provided file path
query = read_query_from_file(query_file_path)

# Access destination dataset and table from Argo workflow parameters
destination_dataset = sys.argv[2]
destination_table = sys.argv[3]
write_disposition = bigquery.WriteDisposition.WRITE_APPEND
table_ref = client.dataset(destination_dataset).table(destination_table)
job_config = bigquery.QueryJobConfig(destination=table_ref, write_disposition=write_disposition)
query_job = client.query(query, job_config=job_config)

# Execute the query
query_job = client.query(query)
results = query_job.result()

for row in results:
    print(row)
