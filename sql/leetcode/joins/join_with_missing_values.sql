-- https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/?envType=study-plan-v2&envId=top-sql-50
-- Write your PostgreSQL query statement below
SELECT unique_id, name FROM Employees LEFT OUTER JOIN EmployeeUNI ON Employees.id = EmployeeUNI.id OR EmployeeUNI.unique_id is null