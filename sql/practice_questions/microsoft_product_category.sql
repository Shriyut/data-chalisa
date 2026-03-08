-- https://datalemur.com/questions/supercloud-customer

--A Microsoft Azure Supercloud customer is defined as a customer who has purchased at least one product from every product category listed in the products table.
--
--Write a query that identifies the customer IDs of these Supercloud customers.

--customer_contracts Table:
--Column Name	Type
--customer_id	integer
--product_id	integer
--amount	integer
--customer_contracts Example Input:
--customer_id	product_id	amount
--1	1	1000
--1	3	2000
--1	5	1500
--2	2	3000
--2	6	2000

--products Table:
--Column Name	Type
--product_id	integer
--product_category	string
--product_name	string
--products Example Input:
--product_id	product_category	product_name
--1	Analytics	Azure Databricks
--2	Analytics	Azure Stream Analytics
--4	Containers	Azure Kubernetes Service
--5	Containers	Azure Service Fabric
--6	Compute	Virtual Machines
--7	Compute	Azure Functions

-- Example Output
--customer_id
--1


-- BRUTE FORCE APPROACH

WITH super_customer AS (
  SELECT
    customers.customer_id AS cust_id,
    COUNT(DISTINCT products.product_category) AS category_count
  FROM customer_contracts AS customers
  INNER JOIN products
    ON customers.product_id = products.product_id
  GROUP BY customers.customer_id
)

SELECT
  cust_id
FROM super_customer
WHERE category_count = (
  SELECT COUNT(DISTINCT product_category) FROM products
)