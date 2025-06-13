PROJECT_ID=""
INSTANCE_ID="hnb-cluster-test"
TABLE_ID="latency_test_table"

echo "Deleting all rows from $TABLE_ID..."
cbt -project $PROJECT_ID -instance $INSTANCE_ID deleteallrows $TABLE_ID
echo "All rows deleted from $TABLE_ID."