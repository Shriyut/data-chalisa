-- select first name, last name, salary, and department names for all employees
-- then use row number to order by salary

SELECT
	e.first_name,
	e.last_name,
	e.salary,
	d.department_name,
	ROW_NUMBER() OVER ( ORDER BY e.salary)
FROM employees e
INNER JOIN departments d ON d.department_id = e.department_id

--  partition by department name and order by salary

SELECT
	e.first_name,
	e.last_name,
	e.salary,
	d.department_name,
	ROW_NUMBER() OVER ( PARTITION BY d.department_name ORDER BY e.salary)
FROM employees e
INNER JOIN departments d ON d.department_id = e.department_id

--  get second highest salary per department

SELECT * FROM (
SELECT
	e.first_name,
	e.last_name,
	e.salary,
	d.department_name,
	ROW_NUMBER() OVER ( PARTITION BY d.department_name ORDER BY e.salary DESC) AS row_num
FROM employees e
INNER JOIN departments d ON d.department_id = e.department_id) AS T
WHERE T.row_num = 2

-- get departments for each salary band with hghest salary

-- get all distinct salaries and assign row num

SELECT
	DISTINCT salary,
	ROW_NUMBER() OVER ( ORDER BY salary)
FROM employees
ORDER BY salary DESC

-- above query returns duplicate records even when distinct is used
-- the reason is that the ROW_NUMBER() operates on the result set BEFORE the DISTINCT is applied
-- its better to use sub queries

SELECT
	salary,
	ROW_NUMBER() OVER ( ORDER BY salary DESC)
FROM
(SELECT
	DISTINCT salary
FROM employees
) AS T

-- pagination technique

-- select first name, last name, salary and department names for all employess and then use ROW_NUMBER to;
-- partition by department name and order by salary and select the five rows starting at #6

SELECT
	*
FROM
(
SELECT
	e.first_name,
	e.last_name,
	e.salary,
	d.department_name,
	ROW_NUMBER() OVER ( PARTITION BY d.department_name ORDER BY e.salary) as row_num
FROM employees e
INNER JOIN departments d ON d.department_id = e.department_id
) AS T
WHERE row_num BETWEEN 6 AND 10

-- Using OVER() to calculate percentage

SELECT
	first_name,
	salary,
	salary / SUM(salary) OVER () * 100
FROM employees

--  calculate difference compared to average

SELECT
	first_name,
	salary,
	salary - AVG(salary) OVER () AS diff,
	AVG(salary) OVER () AS total_avg_salary
FROM employees

-- CUmulative toal using window functions

SELECT
	first_name,
	salary,
	SUM(salary) OVER (),
	SUM(salary) OVER ( ORDER BY salary DESC
	ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) -- EXCLUDES CURRENT ROW
FROM employees

-- COmparing with next value

SELECT
	first_name,
	salary,
	salary - LEAD(salary,1) OVER ( ORDER BY salary DESC) as diff
FROM employees
ORDER BY salary DESC

--  COmpare the salary difference between first and second highest salary per department

SELECT DISTINCT department_id FROM employees
SELECT DISTINCT department_name, department_id FROM departments

SELECT
	-- salary - LEAD(salary,1) OVER (
	-- 	PARTITION BY dpt_name
	-- 	ORDER BY salary DESC
	-- ) as diff,
	-- salary AS cur_Salary,
	-- LEAD(salary,1) OVER (
	-- 	PARTITION BY dpt_name
	-- 	ORDER BY salary DESC
	-- ) AS next_Salary,
	dpt_name,
	COALESCE(salary - LEAD(salary,1) OVER (
		PARTITION BY dpt_name
		ORDER BY salary DESC
	), salary) as diff
FROM (
		SELECT
			e.salary AS salary,
			d.department_name AS dpt_name,
			ROW_NUMBER() OVER (
				PARTITION BY d.department_id
				ORDER BY e.salary DESC
			) as row_num
		FROM employees e
		INNER JOIN departments d ON e.department_id = d.department_id
)
WHERE row_num <=2

-- get second highest salary
WITH salary_tmp AS (
	SELECT
	e.salary,
	d.department_name,
	DENSE_RANK() OVER (
		PARTITION BY e.department_id
		ORDER BY salary DESC
	) as salary_rank
	FROM employees e
	INNER JOIN departments d
	ON e.department_id = d.department_id
),
high_salary AS (
	SELECT * FROM salary_tmp WHERE salary_rank = 1
),
second_salary AS (
	SELECT * FROM salary_tmp WHERE salary_rank = 2
)
SELECT high_salary.salary - second_salary.salary, high_salary.department_name
FROM high_salary
JOIN second_salary USING (department_name)


SELECT
	COALESCE(e.salary - LEAD(e.salary,1) OVER (
	PARTITION BY d.department_id
	ORDER BY salary DESC
	), salary )as DIFF,
	d.department_name
FROM employees e
INNER JOIN departments d ON e.department_id = d.department_id

--  COmpare to lowest paid employee

SELECT
	first_name,
	salary,
	SALARY - LAST_VALUE(salary) OVER W as DIFF,
	(SALARY - LAST_VALUE(salary) OVER W)/ LAST_VALUE(salary) OVER W * 100 as prctnge
FROM employees
WINDOW W AS (ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING )

-- GET DIFF BETWEEN HIGHEST AND LOWEST SLAARY PER DEPARTMENT

SELECT distinct department_id, diff FROM (
SELECT
	department_id,
	FIRST_VALUE(salary) OVER W - LAST_VALUE(salary) OVER W as DIFF,
	(SALARY - LAST_VALUE(salary) OVER W)/ LAST_VALUE(salary) OVER W * 100 as prctnge
FROM employees
WINDOW W AS (
PARTITION BY department_id
ORDER BY salary DESC
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING )
)

SELECT distinct department_id FROM employees

--  RANK VS DENSE_RANK

SELECT
	first_name,
	salary,
	RANK() OVER W, -- skips next value by n if n rows have same rank
	DENSE_RANK() OVER W -- doesnot skip ranks, n element have same rank then next element
FROM employees
WINDOW W AS ( ORDER BY salary DESC)

-- RANK AND GLOBAL RANK

SELECT
	first_name,
	salary,
	department_id,
	RANK() OVER w_department,
	RANK() OVER w_all_departments
FROM employees
WINDOW
	w_department AS ( PARTITION BY department_id ORDER BY salary DESC),
	w_all_departments AS (ORDER BY salary DESC)
ORDER BY department_id, salary DESC

--  Partition by for grouping averages

SELECT
	first_name,
	salary,
	department_id,
	ROUND(AVG(salary) OVER (PARTITION BY department_id),2) AS avg,
	salary - AVG(salary) OVER (PARTITION BY  department_id) AS diff_avg
FROM employees


--  generating sample data using with
WITH names(id, val, test) AS (
	VALUES
	(1,2,3),
	(3,4,5)
)
select * from names