#!/bin/bash

PROJECT_ID=""
INSTANCE_ID="hnb-cluster-test"
TABLE_ID="tds_sim"
REGEX_FILTER="^[^#]*#ACCT-000000#"

START_TIME=$(date +%s)

cbt -project $PROJECT_ID -instance $INSTANCE_ID read $TABLE_ID regex="$REGEX_FILTER"
# regex flag not supported in cbt read command

END_TIME=$(date +%s)

DURATION=$((END_TIME - START_TIME))

TOTAL_RECORDS=$(cbt -project $PROJECT_ID -instance $INSTANCE_ID count $TABLE_ID regex=$REGEX_FILTER)

echo "Total duration to scan records matching regex '${REGEX_FILTER}': ${DURATION} seconds"
echo "Total number of records scanned matching regex '${REGEX_FILTER}': ${TOTAL_RECORDS}"