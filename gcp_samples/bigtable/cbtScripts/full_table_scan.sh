#!/bin/bash

PROJECT_ID=""
INSTANCE_ID="hnb-cluster-test"
TABLE_ID="tds_sim"

cbt -project $PROJECT_ID -instance $INSTANCE_ID ls

START_TIME=$(date +%s)

cbt -project $PROJECT_ID -instance $INSTANCE_ID read $TABLE_ID

END_TIME=$(date +%s)

DURATION=$((END_TIME - START_TIME))

TOTAL_RECORDS=$(cbt -project $PROJECT_ID -instance $INSTANCE_ID count $TABLE_ID)

# Print the total duration and number of records
echo "Total duration to scan the table: ${DURATION} seconds"
echo "Total number of records scanned: ${TOTAL_RECORDS}"