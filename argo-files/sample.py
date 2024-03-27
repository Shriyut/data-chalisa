from google.cloud import bigquery


def query_and_write(project_id, source_dataset_id, source_table_name, dest_dataset_id, dest_table_name, query):
    """
    Executes a BigQuery query and writes the result to a separate table.

    Args:
        project_id (str): Your Google Cloud project ID.
        source_dataset_id (str): ID of the dataset containing the source table.
        source_table_name (str): Name of the source table.
        dest_dataset_id (str): ID of the dataset for the destination table.
        dest_table_name (str): Name of the destination table.
        query (str): The BigQuery SQL query to be executed.
    """

    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # Construct the query job
    query_job = client.query(query)

    # Define the destination table schema (optional)
    # Replace with the actual schema if your destination table requires a specific schema
    destination_table = bigquery.Table(
        table_ref=client.dataset(dest_dataset_id, project=project_id).table(dest_table_name)
    )

    # Set write disposition
    # WRITE_APPEND: Append to existing data (if table exists)
    # WRITE_TRUNCATE: Overwrite existing data (if table exists)
    # WRITE_EMPTY: Fail if the destination table already exists
    # CREATE_IF_NEEDED: Create the destination table if it doesn't exist
    query_job.destination = destination_table
    query_job.write_disposition = bigquery.WriteDisposition.CREATE_IF_NEEDED

    # Execute the query
    query_results = query_job.result()

    # Print confirmation message
    table_ref = query_results.destination_table
    dataset_id = table_ref.dataset_id
    table_id = table_ref.table_id
    print(f"Query results written to table: {project_id}.{dataset_id}.{table_id}")

    # Optional: Iterate through results (if needed)
    # for row in query_results:
    #   # Access row data
    #   print(row)


# Replace with your project ID, dataset and table names, and query
project_id = "your-project-id"
source_dataset_id = "your_source_dataset"
source_table_name = "your_source_table"
dest_dataset_id = "your_dest_dataset"
dest_table_name = "your_dest_table"

# Example query (replace with your actual query)
query = f"""
SELECT * FROM `{project_id}.{source_dataset_id}.{source_table_name}`
"""

# Call the function
query_and_write(project_id, source_dataset_id, source_table_name, dest_dataset_id, dest_table_name, query)
