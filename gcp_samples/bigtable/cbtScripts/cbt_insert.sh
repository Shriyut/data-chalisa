REV_TS=$(python -c "import time; print(9223372036854775807 - int(time.time() * 1_000_000))")

ROWKEY="100010001#${REV_TS}#ACH#txn_id"

cbt -project=$PROJECT_ID -instance=hnb-demo-orals set cbt-testing \
  "$ROWKEY" \
  "cf-ach:achFileID=fileID@$REV_TS" \
  "cf-account:accountId=100010001@$REV_TS"