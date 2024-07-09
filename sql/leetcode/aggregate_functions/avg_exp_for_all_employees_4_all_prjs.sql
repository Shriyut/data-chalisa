-- https://leetcode.com/problems/project-employees-i/?envType=study-plan-v2&envId=top-sql-50

-- Write your PostgreSQL query statement below
SELECT distinct project_id, ROUND(SUM(experience_years)/COUNT(Project.Employee_id)::numeric, 2) as average_years FROM Project
LEFT JOIN Employee ON Project.employee_id = Employee.employee_id
GROUP BY project_id

-- more optimized solution
select p.project_id,
round(avg(e.experience_years),2) as average_years
from Employee e
inner join Project p
on p.employee_id = e.employee_id
group by p.project_id