import json
import os

output_file_path = "/tmp/run_date.txt"
pubsub_msg = sys.argv[1]
msg_obj = json.loads(pubsub_msg)
print(msg_obj["run_date"])
run_date = msg_obj["run_date"]
with open(output_file_path, "w") as file:
    print("Writing run_Date to output file")
    file.write(run_date)