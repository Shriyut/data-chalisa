--https://leetcode.com/problems/rising-temperature/?envType=study-plan-v2&envId=top-sql-50


--solution with o(N) time complexity
-- Write your PostgreSQL query statement below
SELECT id as Id FROM Weather t1 where t1.temperature > (SELECT t2.temperature FROM Weather t2 WHERE recordDate=(t1.recordDate - INTERVAL '1 day'))
--self join would've been useful here

-- O(NlogN) time complexity
SELECT w1.id
from Weather w1
RIGHT JOIN Weather w2
ON w1.recordDate = w2.recordDate+1
WHERE w1.temperature > w2.temperature