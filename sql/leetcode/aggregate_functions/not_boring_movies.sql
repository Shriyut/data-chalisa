-- https://leetcode.com/problems/not-boring-movies/?envType=study-plan-v2&envId=top-sql-50
SELECT id, movie, description, rating FROM Cinema c
WHERE id %2 != 0 AND c.description != 'boring'
ORDER BY rating DESC

--more optimized solution

select * from cinema where id%2 != 0 and description not in ('boring') order by rating desc