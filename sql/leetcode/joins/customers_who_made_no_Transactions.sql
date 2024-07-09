-- https://leetcode.com/problems/customer-who-visited-but-did-not-make-any-transactions/?envType=study-plan-v2&envId=top-sql-50

-- Time complexity O(V+T)
SELECT Visits.customer_id, COUNT(1) as count_no_trans FROM Visits WHERE visit_id NOT IN (
SELECT distinct Visits.visit_id FROM Transactions LEFT OUTER JOIN Visits ON Visits.visit_id = Transactions.visit_id
) GROUP BY Visits.customer_id;
-- no need for left outer join in the above query

-- Solution with o(n^2) complexity
SELECT customer_id, count(*) as count_no_trans
FROM Visits
WHERE visit_id NOT IN (SELECT distinct visit_id FROM Transactions)
GROUP BY customer_id