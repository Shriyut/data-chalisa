import pandas as pd
from google.cloud import bigquery

project_id = "us-gcp-ame-con-ff12d-npd-1"
src_dataset = "audit_dataset"
dest_dataset = "sj_audit_dataset"
tables = [
    "batch_failed_transactions",
    "batch_patching_audit_log",
    "file_metadata",
    "batch_prdnd_ref",
    "prdnd_recon",
    "prdnd_recon_isslog",
    "stream_patching_audit_log",
    "stream_fail_tran",
    "window_metadata"
]

client = bigquery.Client(project=project_id)

for table in tables:
    src_table = f"{project_id}.{src_dataset}.{table}"
    dest_table = f"{project_id}.{dest_dataset}.{table}"

    print(f"Migrating {src_table} to {dest_table}...")

    src_table_ref = client.get_table(src_table)
    schema = src_table_ref.schema
    dest_table_ref = bigquery.Table(dest_table, schema=schema)
    try:
        client.create_table(dest_table_ref)
    except Exception:
        pass  # Table may already exist

    df = client.query(f"SELECT * FROM `{src_table}`").to_dataframe()
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        schema=schema
    )
    client.load_table_from_dataframe(df, dest_table, job_config=job_config, location="us-central1").result()

print("Migration complete.")