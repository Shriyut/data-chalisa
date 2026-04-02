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