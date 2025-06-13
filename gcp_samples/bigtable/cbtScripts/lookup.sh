#!/bin/bash

PROJECT_ID=""
INSTANCE_ID="hnb-cluster-test"
TABLE_ID="tds_sim"
#ROW_KEY="2025-05-06 08:53:55.599248#ACCT-000000#CREATED#0b5a0af4-ac40-4e09-83c4-a454f5b051bc"
ROW_KEY="ACCT-000000#2025-05-06 08:53:55.599248#CREATED#0b5a0af4-ac40-4e09-83c4-a454f5b051bc"
echo "Performing lookup for row key: $ROW_KEY in table: $TABLE_ID"

{ time cbt -project=$PROJECT_ID -instance=$INSTANCE_ID lookup $TABLE_ID $ROW_KEY; } 2> timing.txt

echo "Timing information:"
cat timing.txt