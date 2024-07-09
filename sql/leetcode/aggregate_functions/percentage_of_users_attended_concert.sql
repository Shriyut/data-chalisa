-- https://leetcode.com/problems/percentage-of-users-attended-a-contest/description/?envType=study-plan-v2&envId=top-sql-50

--Solution
-- Write your PostgreSQL query statement below

WITH base AS (
   SELECT contest_id, COUNT(user_id) as cont_user_count FROM Register
    GROUP BY contest_id
),
count_rec AS (
    SELECT COUNT(user_id) as user_count FROM Users
)
SELECT contest_id, ROUND(((cont_user_count*100)::float/user_count::float)::numeric, 2) as percentage FROM base
INNER JOIN count_rec ON 1=1
ORDER BY percentage DESC, contest_id ASC;
--to much casting applied in above solution and CTEs used unnecessarily

--more optimized solution
select contest_id,
       ROUND((count(distinct user_id)::numeric / (select count(distinct user_id) from Users)) * 100 , 2) as percentage
    from Register
    group by contest_id
    having count(distinct user_id) > 0
    order by percentage desc, contest_id asc;