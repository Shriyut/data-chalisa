from google.cloud import bigtable
from google.cloud.bigtable.row import DirectRow
from google.cloud.bigtable.row_set import RowSet
from google.cloud.bigtable_v2.types import data
from google.cloud.bigtable_v2.types.data import Mutation
# from google.cloud.bigtable_v2.types.data import
import json
import datetime
from payment_processing_main import convert_msg_to_bigtable_row

project_id = "us-gcp-ame-con-ff12d-npd-1"
instance_id = "hnb-demo-orals"
table_id = "payments-test"
row_key = "CUS0000#CARD#2025-02-14#INITIATED"


def read_row_from_bigtable(project_id, instance_id, table_id, row_key):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    total_versions = None
    latest_cell = None
    direct_row = None
    row = table.read_row(row_key.encode('utf-8'))

    if row:

        direct_row = DirectRow(row_key.encode('utf-8'))

        for column_family_id, columns in row.cells.items():

            for column, cells in columns.items():
                latest_cell = cells[0]
                # for cell in cells: TODO: Check how to get version history - gives entire history not just latest
                #  record print( f"Column family: {column_family_id}, Column: {column.decode('utf-8')},
                #  Value: {cell.value.decode('utf-8')}, Timestamp: {cell.timestamp}") total_versions = len(cells)
                direct_row.set_cell(
                    column_family_id,
                    column.decode('utf-8'),
                    latest_cell.value.decode('utf-8'),
                    timestamp=latest_cell.timestamp
                )
                # print(
                #     f"Latest cf: {column_family_id}, Column: {column.decode('utf-8')}, Value: {latest_cell.value.decode('utf-8')}, Timestamp: {latest_cell.timestamp}")
    else:
        print(f"Not found: {row_key}")

    # print(f"Total number of cell versions are {total_versions}")
    # print(type(latest_cell)) # <class 'google.cloud.bigtable.row.Cell'>
    return direct_row


def sample_reconciliation(project_id, instance_id, table_id, row_key):
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    row = table.read_row(row_key.encode('utf-8'))

    json_string = """{"payment_id": "653aa529-e63b-41b7-bcf8-6a684d070c99", "payment_type": "CARD", "direction": "DEBIT", "version": "1.0", "created_at": "2025-02-14T13:40:57.667964", "updated_at": "2025-02-14T13:40:57.667964", "status": "INITIATED", "amount": {"value": "25", "currency": "AUD", "exchange_info": null}, "originator": {"party_type": "INDIVIDUAL", "party_id": "CUS0000", "name": "Dawson, Austin and Hardy", "account_info": {"account_id": "ACC9970", "account_type": "CHECKING", "routing_info": {"type": "ABA", "value": "865905248"}}, "contact_info": {"address": {"street": "789 Oak St", "city": "Lake David", "state": "California", "postal_code": "90210", "country": "JP"}, "electronic": {"email": "user1701@example.com", "phone": "+1-445-190-2312"}}}, "beneficiary": {"party_type": "CORPORATE", "party_id": "CUST9887", "name": "Smith and Sons", "account_info": {"account_id": "ACC5656", "account_type": "CHECKING", "routing_info": {"type": "ABA", "value": "704537099"}}, "contact_info": {"address": {"street": "789 Oak St", "city": "Springfield", "state": "Oregon", "postal_code": "01103", "country": "JP"}, "electronic": {"email": "user6177@test.com", "phone": "+1-447-389-1286"}}}, "processing": {"priority": "NORMAL", "processing_window": "SAME_DAY", "submission_date": "2025-02-14T13:40:57.667964", "effective_date": "2025-02-14T14:40:57.667964", "settlement_date": "2025-02-14T15:40:57.667964", "status_tracking": {"history": []}}, "references": {}, "remittance_info": {}, "type_specific_data": {"wire_type": "DOMESTIC", "message_type": "MT103", "intermediary_bank": null, "charges": {"type": "OUR"}}, "regulatory": {}, "metadata": {}, "card_present": false, "entry_mode": "CONTACTLESS", "network": "AMEX"}
"""

    #     convert json string to direct row format
    simulated_bytes = json_string.encode("utf-8")
    simulated_input = json.loads(simulated_bytes.decode("utf-8"))

    transformed_input_record = convert_msg_to_bigtable_row(simulated_input)

    # print(type(transformed_input_record)) # DirectRow

    bigtable_record = read_row_from_bigtable(project_id, instance_id, table_id, row_key)

    # print(type(bigtable_record)) # DirectRow

    # if transformed_input_record == bigtable_record:
    #     print("Duplicate") #equality operation for the same msg equates to false -same as java - likely order mismatch
    # else:
    #     print("Mismatch")
    #
    # print("Transformed Input Record:", transformed_input_record.__dict__)
    # print("Bigtable Record:", bigtable_record.__dict__)

    # print(transformed_input_record.__dict__["_pb_mutations"])
    # print(type(transformed_input_record.__dict__["_pb_mutations"]))
    #
    # print(transformed_input_record.__dict__["_pb_mutations"])
    # print(bigtable_record.__dict__["_pb_mutations"])

    # print(type(input_msg_list[0])) # <class 'google.cloud.bigtable_v2.types.data.Mutation'> for both
    # print(type(bigtable_record_list[0]))

    # input_msg_list[0].set_cell.family_name

    # print(input_msg_list[0])
    # print(bigtable_record_list[0])

    # if input_msg_list[0] == bigtable_record_list[0]: amount info compared with payment info - created at
    #     print("Duplicate") # cant take one for one mapping - need to compare all values

    input_msg_list = transformed_input_record.__dict__["_pb_mutations"]  # TODO: Check how this can be optimized
    bigtable_record_list = bigtable_record.__dict__["_pb_mutations"]

    input_msg_mutation_dict = extract_families(input_msg_list)
    bigtable_record_mutation_dict = extract_families(bigtable_record_list)

    print(input_msg_mutation_dict)
    print(bigtable_record_mutation_dict)

    final_check = input_msg_mutation_dict == bigtable_record_mutation_dict
    print(final_check)

    if final_check:
        print("Records are totally duplicate")
        # yield invalid tag for totally duplicate record
    else:
        # ignoring situations where families can be different since mutation object is built in the pipeline
        differences = check_for_differences(input_msg_mutation_dict, bigtable_record_mutation_dict)
        print("There are some changes in the record")
        print(differences.__repr__())
        # yield updated directrow to be written

        current_timestamp = datetime.datetime.now()

        for family, qualifiers in differences.items():

            for qualifier, (new_value, _) in qualifiers.items():
                # Update record read from bigtable here
                bigtable_record.set_cell(
                    family,
                    qualifier,
                    new_value,
                    timestamp=current_timestamp
                )

        bigtable_record._table = table  # needed for commit method
        bigtable_record.commit()  # use yield in pipeline for record
        print("Updated value in bigtable")


def extract_families(mutations):
    families = {}

    for mutation in mutations:

        set_cell = mutation.set_cell
        family_name = set_cell.family_name
        column_qualifier = set_cell.column_qualifier
        value = set_cell.value

        if family_name not in families:
            families[family_name] = {}

        families[family_name][column_qualifier] = value

    return families


def check_for_differences(input_msg_dict, bigtable_record_dict):
    differences = {}

    for family in input_msg_dict.keys() | bigtable_record_dict.keys():

        for column_qualifier in input_msg_dict[family].keys() | bigtable_record_dict[family].keys():

            if input_msg_dict[family][column_qualifier] != bigtable_record_dict[family][column_qualifier]:
                if family not in differences:
                    differences[family] = {}

                differences[family][column_qualifier] = (
                    input_msg_dict[family][column_qualifier], bigtable_record_dict[family][column_qualifier])

    return differences


def print_row(row):
    print("Reading data for {}:".format(row.row_key.decode("utf-8")))
    for cf, cols in sorted(row.cells.items()):
        print("Column Family {}".format(cf))
        for col, cells in sorted(cols.items()):
            for cell in cells:
                labels = (
                    " [{}]".format(",".join(cell.labels)) if len(cell.labels) else ""
                )
                print(
                    "\t{}: {} @{}{}".format(
                        col.decode("utf-8"),
                        cell.value.decode("utf-8"),
                        cell.timestamp,
                        labels,
                    )
                )
    print("")


def print_row_key(row):
    print("Reading data for {}:".format(row.row_key.decode("utf-8")))


def prefix_test(row_key):
    prefix = row_key.rpartition('#')[2]
    print(f"Prefix: {prefix}")


def order_validation(project_id, instance_id, table_id, row_key):
    bigtable_record = read_row_from_bigtable(project_id, instance_id, table_id, row_key)

    if bigtable_record is not None:
        print("None")
        pass
    else:
        # order validation to be performed here
        client = bigtable.Client(project=project_id, admin=True)
        instance = client.instance(instance_id)
        table = instance.table(table_id)

        prefix = row_key.rpartition('#')[0]
        print(prefix)
        initiate_key = prefix+"#INITIATED"
        processing_key = prefix+"#PROCESSING"
        received_key = prefix+"#RECEIVED"

        row_set = RowSet()
        row_set.add_row_key(initiate_key.encode('utf-8'))
        row_set.add_row_key(processing_key.encode('utf-8'))
        row_set.add_row_key(received_key.encode('utf-8'))

        message_status = row_key.rpartition('#')[2]

        try:
            status_values = []
            rows = table.read_rows(row_set=row_set)
            for record_row in rows:
                status_values.append(record_row.row_key.decode('utf-8').rpartition('#')[2])
            print(status_values.__repr__())
            for row in rows:
                print_row_key(row)

            if "RECEIVED" == message_status and "PROCESSING" in status_values and "INITIATED" in status_values and len(
                    status_values) == 2:
                print("Valid")
            elif "PROCESSING" == message_status and "INITIATED" in status_values and len(status_values) == 1:
                print("Valid")
            elif "INITIATED" == message_status and len(status_values) == 0:
                print("Valid")
            else:
                print("InValid")
        except Exception as e:
            print(e)

        # initiated_bigtable_record = read_row_from_bigtable(project_id, instance_id, table_id, initiate_key)
        # processing_bigtable_record = read_row_from_bigtable(project_id, instance_id, table_id, processing_key)
        # received_bigtable_record = read_row_from_bigtable(project_id, instance_id, table_id, received_key)
        #
        # order_check = False
        #
        # if initiated_bigtable_record is not None:
        #     pass
        # # end_key = "CUS0000#CARD#2025-02-14#RECEIVED"
        # end_key = prefix + "#RECEIVED"
        #
        # row_set = RowSet()
        # row_set.add_row_range_from_keys(start_key=prefix.encode("utf-8"), end_key=end_key.encode("utf-8"),
        #                                 end_inclusive=True)
        #
        # # row_set.add_row_range_from_keys(start_key=prefix.encode("utf-8")) # prints all rows
        #
        # rows = table.read_rows(row_set=row_set)
        # for row in rows:
        #     # print_row_key(row)
        #     print(row.row_key.decode('utf-8'))

        # from google.cloud.bigtable import row_filters
        # # # row = table.direct_row(row_key)
        # # # print(row)
        # # row_filter = bigtable.row_filters.CellsColumnLimitFilter(1) # to get the latest cell version only
        # # row = table.read_row(row_key, row_filter)
        # # print_row(row)
        #
        # rows = table.read_rows(
        #     filter_=row_filters.RowKeyRegexFilter(f"^{prefix}".encode("utf-8"))
        # )
        # for row in rows:
        #     print_row(row)





# read_row_from_bigtable(project_id, instance_id, table_id, row_key)
# sample_reconciliation(project_id, instance_id, table_id, row_key)
new_row_key = "CUS0001#CARD#2025-02-14#INITIATED"
new_row_key1 = "CUS0001#CARD#2025-02-14#PROCESSING"
order_validation(project_id, instance_id, table_id, new_row_key1)
# prefix_test(row_key)
