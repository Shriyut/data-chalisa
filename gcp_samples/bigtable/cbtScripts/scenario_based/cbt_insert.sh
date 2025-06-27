#!/bin/bash

PROJECT="your gcp project id"
INSTANCE="tds-design"
TABLE="tds_patching_test"

MICROS=$(date +%s%6N)
MAX_VALUE=9223372036854775807
REVERSED_MICROS=$(awk -v max="$MAX_VALUE" -v micros="$MICROS" 'BEGIN {print max - micros}')
echo "Current microseconds: $MICROS"
echo "Reversed microseconds: $REVERSED_MICROS"

RAND_SUFFIX=$(python3 -c "import random; print(random.randint(10000, 99999))")

TRANSACTION_TYPE="ACH"
ACCOUNT_ID="A12345"
TO_ACCOUNT_ID="B67890"
TO_SRC_REF="SRC987"
FROM_SRC_REF="SRC123"
CORRELATION_ID="crln-id-1"
IDEMPOTENCY_KEY="unique-key-1"
ACCOUNT_TRANSACTION_ID="transaction-id-${RAND_SUFFIX}"
PERIOD_REFERENCE=$(date +%Y%m%d)
NOW_TS=$(date +%Y-%m-%dT%H:%M:%S.%3N)
MESSAGE_JSON="{\"toAccount_accountId\":\"$TO_ACCOUNT_ID\",\"toAccount_srcTransactionReference\":\"$TO_SRC_REF\",\"fromAccount_AccountId\":\"$ACCOUNT_ID\",\"fromAccount_sourceTransactionReference\":\"$FROM_SRC_REF\"}"
ROWKEY="${ACCOUNT_ID}#${REVERSED_MICROS}#${TRANSACTION_TYPE}#${ACCOUNT_TRANSACTION_ID}"

cbt -project=$PROJECT -instance=$INSTANCE set $TABLE $ROWKEY \
  cf-account:toAccount="{\"toAccount_accountId\":\"$TO_ACCOUNT_ID\",\"toAccount_srcTransactionReference\":\"$TO_SRC_REF\"}" \
  cf-account:fromAccount="{\"fromAccount_AccountId\":\"$ACCOUNT_ID\",\"fromAccount_sourceTransactionReference\":\"$FROM_SRC_REF\"}" \
  cf-account:accountId="$ACCOUNT_ID" \
  cf-account:sourceTransactionReference="$ACCOUNT_TRANSACTION_ID"

cbt -project=$PROJECT -instance=$INSTANCE set $TABLE $ROWKEY \
  cf-metadata:soft-delete="False" \
  cf-metadata:message="$MESSAGE_JSON" \
  cf-metadata:correlationId="$CORRELATION_ID" \
  cf-metadata:peiordReference="$PERIOD_REFERENCE" \
  cf-metadata:lastUpdateTimestamp="$NOW_TS" \
  cf-metadata:idempotencyKey="$IDEMPOTENCY_KEY"

cbt -project=$PROJECT -instance=$INSTANCE set $TABLE $ROWKEY \
  cf-transaction:accountTransaactionId="$ACCOUNT_TRANSACTION_ID" \
  cf-transaction:transactionAmount="1000.00" \
  cf-transaction:currenyCode="USD" \
  cf-transaction:transactionType="ACH" \
  cf-transaction:statementDescriptor="Credit Card Bill" \
  cf-transaction:transactionTimestamp="$NOW_TS" \
  cf-transaction:transactionSource="SFTP" \
  cf-transaction:transactionStatus="INITIATED" \
  cf-transaction:postingDate=""

PATCHING_ID="patch$(date +%Y%m%d%H%M%S%6N)"


# Generating mock hogan entry
read DIN_NUMBER SERIAL_NUMBER <<< $(python3 -c "import random; print(random.randint(1000, 109999), 'SN'+str(random.randint(10000, 1099999)))")

PRODUCT_CODE="prd_cd_${RAND_SUFFIX}"
TRANSACTION_ID="hogan-transaction-test-id_${RAND_SUFFIX}"
NOW_TS=$(date +%Y-%m-%dT%H:%M:%S.%3N)

MESSAGE_JSON="{\"dinNumber\":$DIN_NUMBER,\"product_code\":\"$PRODUCT_CODE\",\"serial_number\":\"$SERIAL_NUMBER\",\"transactionId\":\"$TRANSACTION_ID\"}"
HG_ROWKEY="${ACCOUNT_ID}#${TRANSACTION_TYPE}#${TRANSACTION_ID}"

cbt -project=$PROJECT -instance=$INSTANCE set tds_hg_mock $HG_ROWKEY \
  cf-content:dinNumber="$DIN_NUMBER" \
  cf-content:product_code="$PRODUCT_CODE" \
  cf-content:serial_number="$SERIAL_NUMBER" \
  cf-content:transactionId="$TRANSACTION_ID" \
  cf-content:accountId="$ACCOUNT_ID" \
  cf-content:transactionType="$TRANSACTION_TYPE"

cbt -project=$PROJECT -instance=$INSTANCE set tds_hg_mock $HG_ROWKEY \
  cf-metadata:soft-delete="false" \
  cf-metadata:message="$MESSAGE_JSON" \
  cf-metadata:periodReference="$PERIOD_REFERENCE" \
  cf-metadata:lastUpdateTimestamp="$NOW_TS"

# populating the lookup table
LOOKUP_ROWKEY="${ACCOUNT_ID}#${DIN_NUMBER}"
cbt -project=$PROJECT -instance=$INSTANCE set tds_lookup_test $LOOKUP_ROWKEY \
  cf-rowkey:tds_rowkey="$ROWKEY" \
  cf-rowkey:hogan_rowkey="$HG_ROWKEY"


# use the below block to check for scenarios where tds_rowkey hasnt been populated yet
#cbt -project=$PROJECT -instance=$INSTANCE set tds_lookup_test $LOOKUP_ROWKEY \
#  cf-rowkey:hogan_rowkey="$HG_ROWKEY"


# Updating the patching audit table
#bq query --use_legacy_sql=false "
#  INSERT INTO \`abc_framework.patching_audit_log\` (
#    patching_id, event_type, resource_id, period_reference, file_id, window_id,
#    tds_lookup_rowkey, posting_Date, status, insert_timestamp, update_timestamp
#  ) VALUES (
#    '$PATCHING_ID', 'ACH', '$ACCOUNT_TRANSACTION_ID', '$PERIOD_REFERENCE', '', '1234',
#    '$LOOKUP_ROWKEY', CURRENT_DATE(), 'ACTIVE', '$NOW_TS', NULL
#  )
#"

bq query --use_legacy_sql=false "
  INSERT INTO \`abc_framework.patching_audit_log\` (
    patching_id, event_type, resource_id, period_reference, file_id, window_id,
    tds_lookup_rowkey, tds_hogan_rowkey, posting_Date, status, insert_timestamp, update_timestamp
  ) VALUES (
    '$PATCHING_ID', 'ACH', '$ACCOUNT_TRANSACTION_ID', '$PERIOD_REFERENCE', '', '1234',
    '$LOOKUP_ROWKEY', '$HG_ROWKEY', CURRENT_DATE(), 'ACTIVE', '$NOW_TS', NULL
  )
"

