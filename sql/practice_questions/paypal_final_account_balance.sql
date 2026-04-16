--https://datalemur.com/questions/final-account-balance

--Given a table containing information about bank deposits and withdrawals made using Paypal, write a query to retrieve the final account balance for each account, taking into account all the transactions recorded in the table with the assumption that there are no missing transactions.
--
--transactions Table:
--Column Name	Type
--transaction_id	integer
--account_id	integer
--amount	decimal
--transaction_type	varchar
--transactions Example Input:
--transaction_id	account_id	amount	transaction_type
--123	101	10.00	Deposit
--124	101	20.00	Deposit
--125	101	5.00	Withdrawal
--126	201	20.00	Deposit
--128	201	10.00	Withdrawal
--Example Output:
--account_id	final_balance
--101	25.00
--201	10.00

SELECT
  account_id,
  SUM(
    CASE
      WHEN transaction_type = 'Deposit' THEN amount ELSE -amount
    END) AS final_balance
  FROM transactions
  GROUP BY account_id


SELECT
  account_id,
  SUM(
    CASE
      WHEN transaction_type = 'Deposit' THEN amount
      WHEN transaction_type = 'Withdrawal' THEN -amount
    END
  ) AS final_balance
FROM transactions
GROUP BY account_id;


-- If certain accounts have disproportionately more transactions (data skew):
-- Two-phase aggregation to handle skew
SELECT
  account_id,
  SUM(partial_balance) AS final_balance
FROM (
  SELECT
    account_id,
    SUM(IF(transaction_type = 'Deposit', amount, -amount)) AS partial_balance
  FROM `project.dataset.transactions`
  GROUP BY account_id, MOD(transaction_id, 100)  -- break hot keys into 100 buckets
)
GROUP BY account_id;

-- For billion-row tables, storing 'Deposit'/'Withdrawal' as strings is wasteful:

-- Better: Use integer encoding
-- 1 = Deposit, -1 = Withdrawal (acts as multiplier)
SELECT
  account_id,
  SUM(amount * transaction_sign) AS final_balance
FROM `project.dataset.transactions_optimized`
GROUP BY account_id;

--This reduces:
--
--Storage: STRING → INT64 saves ~10 bytes per row × 1B = ~10GB savings
--Compute: No string comparison, just multiplication, which is faster at scale.

