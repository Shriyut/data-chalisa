#!/bin/bash

PROJECT_ID=""
INSTANCE_ID="hnb-cluster-test"
TABLE_ID="tds_sim"
ROWKEY_PREFIX="ACCT-000000"

#cbt -project $PROJECT_ID -instance $INSTANCE_ID ls

START_TIME=$(date +%s)

cbt -project $PROJECT_ID -instance $INSTANCE_ID read $TABLE_ID prefix=$ROWKEY_PREFIX

END_TIME=$(date +%s)

DURATION=$((END_TIME - START_TIME))

TOTAL_RECORDS=$(cbt -project $PROJECT_ID -instance $INSTANCE_ID count $TABLE_ID prefix=$ROWKEY_PREFIX)

# Print the total duration and number of records
echo "Total duration to scan records with prefix '${ROWKEY_PREFIX}': ${DURATION} seconds"
echo "Total number of records scanned with prefix '${ROWKEY_PREFIX}': ${TOTAL_RECORDS}"