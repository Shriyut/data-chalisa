import os
from google.cloud import bigtable

PROJECT_ID = ""
SRC_INSTANCE_ID = "tds-design"
DEST_INSTANCE_ID = "sj-test-instance"
TABLE_ID = "bai_refcd_by_tran_mapping_cd"

def main():
    # Set up Bigtable clients
    src_client = bigtable.Client(project=PROJECT_ID, admin=True)
    dest_client = bigtable.Client(project=PROJECT_ID, admin=True)

    src_instance = src_client.instance(SRC_INSTANCE_ID)
    dest_instance = dest_client.instance(DEST_INSTANCE_ID)

    src_table = src_instance.table(TABLE_ID)
    dest_table = dest_instance.table(TABLE_ID)

    # Ensure destination table exists with correct column families
    if not dest_table.exists():
        print("Creating destination table...")
        column_families = {
            "cf-content": bigtable.column_family.MaxVersionsGCRule(1),
            "cf-metadata": bigtable.column_family.MaxVersionsGCRule(1),
        }
        dest_table.create(column_families=column_families)

    # Read and write rows
    print("Copying rows...")
    rows = src_table.read_rows()
    batch = dest_table.mutations_batcher()
    row_count = 0
    for row in rows:
        new_row = dest_table.direct_row(row.row_key)
        for cf, columns in row.cells.items():
            for col, cells in columns.items():
                for cell in cells:
                    new_row.set_cell(
                        cf, col, cell.value, timestamp=cell.timestamp
                    )
        batch.mutate(new_row)
        row_count += 1
        if row_count % 1000 == 0:
            print(f"Copied {row_count} rows...")

    batch.flush()
    print(f"Copy complete. Total rows copied: {row_count}")

if __name__ == "__main__":
    main()