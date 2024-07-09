-- https://leetcode.com/problems/average-time-of-process-per-machine/?envType=study-plan-v2&envId=top-sql-50


--wrong solution (didnt pass all test cases)
-- Write your PostgreSQL query statement below
SELECT machine_id, SUM(processing_time)/2 as processing_time FROM
(SELECT a1.machine_id, ROUND((a2.timestamp - a1.timestamp/COUNT(a1.process_id))::numeric, 3) as processing_time FROM Activity a1
JOIN Activity a2 ON a1.machine_id = a2.machine_id AND a1.process_id = a2.process_id AND a1.activity_type = 'start' AND a2.activity_type = 'end'
GROUP BY a1.machine_id, a2.timestamp, a1.timestamp, a1.process_id)
GROUP BY machine_id;


--Passed all test cases
SELECT A1.machine_id, ROUND(AVG(A2.timestamp - A1.timestamp)::numeric, 3) AS processing_time
FROM Activity AS A1
JOIN Activity AS A2
ON A1.machine_id = A2.machine_id AND A1.process_id = A2.process_id
AND A1.activity_type = 'start' AND A2.activity_type = 'end'
GROUP BY A1.machine_id;