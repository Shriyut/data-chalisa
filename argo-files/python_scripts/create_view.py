from google.cloud import bigquery, exceptions
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

destination_dataset = sys.argv[3]
view_name = sys.argv[2]
view_ref = client.dataset(destination_dataset).table(view_name)

view_query = query
print(view_query)
try:
    view_creation_obj = bigquery.Table(view_ref)
    view_creation_obj.view_query = view_query
    view_creation_obj.view_use_legacy_sql = False
    client.create_table(view_creation_obj)
except Exception as e:
    print(f"Either the view already exists or some other error: {str(e)}")