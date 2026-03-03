SELECT * FROM trades
SELECT DISTINCT(region) FROM trades
SELECT MIN(year), MAX(year) FROM trades
SELECT DISTINCT(country) FROM trades
SELECT COUNT(DISTINCT(country)) FROM trades

-- average import/exports by region

SELECT AVG(imports) as avg_import, AVG(exports) as avg_export
FROM trades
GROUP BY region

-- Total average imports by each region

SELECT
	region,
	AVG(imports)
FROM trades
GROUP BY region

SELECT
	CASE
		WHEN GROUPING(region) = 1 THEN 'global' ELSE region
	END AS region,
	ROUND(AVG(imports)/1000000,2)
FROM trades
GROUP BY ROLLUP(region)
ORDER BY 2 DESC

-- TOtal average imports by country and region

SELECT
	region,
	country,
	ROUND(AVG(imports)/1000000000,2)
FROM trades
GROUP BY ROLLUP(region,country)
ORDER BY 1

-- THe GROUP BY CUBE allows you to have mu;tiple grouping sets
-- THe query generates all possible grouping sets based on the dimension columns specified
-- if there are n columns in group by cube then you will get n ** 2 combinations

SELECT
	region,
	country,
	ROUND(AVG(imports/1000000),2)
FROM trades
WHERE
	country IN ('USA', 'France', 'Germany', 'Brazil')
GROUP BY
	CUBE(region,country) -- gives global avg, regional avg, country specific avg

-- GROUPING SETS - A GROUPING SET is a set of columns by which you group by using GROUP BY clause
-- GROUPING SETS caluse, you can explicitly list the aggregates you want
-- CUBE and GROUPING SETS help in implementing UNION through the same query


SELECT
	region,
	country,
	ROUND(AVG(imports/1000000),2)
FROM trades
WHERE
	country IN ('USA', 'France', 'Germany', 'Brazil')
GROUP BY
	GROUPING SETS
	(
		(), 	-- global avg
		region, -- regional avg
		country -- country avg
	)

-- FILTER clause allows you to do a selective aggregate
-- It aggregates the group set based on filter condition and allows you to selectively pass data
-- to those aggregations


-- Get avg import for each region for
-- 1. all period, 2. period_year < 1995, 3. period_year >= 1995


SELECT
	region,
	AVG(exports) AS avg_all,
	AVG(exports) FILTER (WHERE year < 1995) AS avg_old,
	AVG(exports) FILTER (WHERE year >= 1995) AS avg_new
FROM trades
GROUP BY
	ROLLUP (region)


-- Aggregate functions - takes many rows and turns them into fewer aggregated rows
-- flattens the data basically

--  A window function compares the current row with all rows in the group
-- aggregate_function OVER ( PARTITION BY group_name)


-- VIew country, year, import, exports and overall average export

SELECT country, year, imports, exports, AVG(exports) OVER() as avg_exports FROM trades
-- above query gives global avg for each row
WITH tmp AS (
SELECT country, year, imports, exports, AVG(exports) OVER() as avg_exports
FROM trades
)
SELECT tmp.country, tmp.year, tmp.exports,
tmp.avg_exports, tmp.avg_exports - tmp.exports AS diff FROM tmp

-------

SELECT country, year, imports, exports,
AVG(exports) OVER() as avg_exports
FROM trades

SELECT
country, year, imports, exports,
AVG(exports) AS avg_exports -- gives export for each row as avg cuz of grp by
FROM trades
GROUP BY
	country, year, imports, exports

SELECT country, year, imports, exports,
AVG(exports) OVER(PARTITION BY country) as avg_exports -- avg export per country of all countries
FROM trades

-- avg export based on year filter
SELECT country, year, imports, exports,
AVG(exports) OVER(PARTITION BY year < 2000) as avg_exports
FROM trades

-- avg export based on year filter
SELECT country, year, imports, exports,
AVG(exports) OVER(PARTITION BY year < 2000, country) as avg_exports
FROM trades

-- format imports and exports
UPDATE trades
SET
imports = ROUND(imports/1000000,2),
exports = ROUND(exports/1000000,2)

SELECT * FROM trades

-- ordering inside windowing functions
-- aggregate_function OVER ( PARTITION BY group_name ORDER BY column)


-- MAX exports for some specific countries for period 2001 onwards
SELECT
	country,
	year,
	exports,
	-- partitions the group per each country and orders it per year
	MIN(exports) OVER (PARTITION BY country ORDER BY year)
	-- MAX(exports) OVER (PARTITION BY country ORDER BY year)
	-- MAX(exports) OVER (PARTITION BY year > 2007 ORDER BY year)
	-- MAX(exports) OVER (PARTITION BY country, year < 2006 ORDER BY country DESC)
FROM trades
WHERE year > 2001 -- with where clause 3002 rows
AND country IN ('USA', 'France')

-- adding year filter with windowing would result in all rows with max based on filter
-- adding WHERE clause explicitly only gives the row that satisfy the filter criteria

-- SLIDING DYNAMIC WINDOWS

-- if window frame is not specified (OVER()), the entire data is takem for the
-- aggregate function

SELECT
	country,
	year,
	exports,
	MIN(exports) OVER (PARTITION BY country ORDER BY year
		-- ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
		-- RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW -- default
		ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING EXCLUDE CURRENT ROW
	) as AVG_MOVING
FROM trades
WHERE year BETWEEN 2001 AND 2010
AND country IN ('USA', 'France')

-- WIndow frames are used to indicate how many rows around the cuurent row
-- the window function should include

SELECT
	*, ARRAY_AGG(X) OVER (ORDER BY X) -- array agg tells us the content of the window being processed
FROM generate_series(1,5) AS X;

-- RANGE can only be used with UNBOUNDED
-- ROWS can actually be used for all of the options

-- If the field you chose for ORDER BY does not contain unique values for each row
-- then RANGE will combine all the rows it comes across for non-unique values
-- rather than procesisng them one at a time

-- ROWS will include all of the rows in the non-unique bunch but processes each of them
-- separately


SELECT
	*,
	X/3 AS Y,
	ARRAY_AGG(X) OVER (
		ORDER BY X ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
	) AS rows1,
	ARRAY_AGG(X) OVER (
		ORDER BY X RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING
	) AS range1,
	ARRAY_AGG(X/3) OVER (
		ORDER BY (X/3) ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
	) AS rows2,
	ARRAY_AGG(X/3) OVER (
		ORDER BY (X/3) RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING
	) AS range2
FROM generate_series(1,10) AS X;

-- WINDOW function allows us to add columns to the result set that has been calculated on the fly
-- Allows to pre-define a result set and use it anywhere in the query

-- SELECT
-- 	WF1() OVER W,
-- 	WF2() OVER W
-- FROM table
-- WINDOW W AS (PARTITION BY C1 ORDER BY C2)

-- Get minimum and maximum exports per year per each country say from year 2000

SELECT
	country,
	year,
	exports,
	MIN(exports) OVER W,
	MAX(exports) OVER W
FROM trades
WHERE
	year > 2000
WINDOW W AS (PARTITION BY country ORDER BY year)
-- WINDOW W AS (PARTITION BY year ORDER BY country)


-- RANK & DENSE_RANK Functions

-- RANK() function returns the number of current row within its window, starting with 1
-- TO avoid duplicate ranks, use DENSE_RANK() function

-- Top 10 exports by year for USA

SELECT
	year,
	exports,
	RANK() OVER (ORDER BY exports DESC) as r
FROM trades
WHERE country = 'USA'
LIMIT 10

-- get fifth highest import

SELECT * FROM (
	SELECT
	year,
	exports,
	RANK() OVER (ORDER BY exports DESC) as r
	FROM trades
	WHERE country = 'USA'
	LIMIT 10
) AS T
WHERE r = 5

-- get top export year for each country
SELECT * FROM
(
SELECT
	country,
	year,
	RANK() OVER ( PARTITION BY country ORDER BY exports DESC) as exp_rank
FROM trades
) AS T
WHERE T.exp_rank = 1

-- old school approach

SELECT
exports, year, t1.country
FROM trades t1
JOIN (
SELECT country, MAX(exports) AS max_exp FROM trades GROUP BY country
) t2
ON t1.country = t2.country
AND t1.exports = t2.max_exp


-- gives max export for each country for each year - i.e. return all rows
SELECT
	country,
	year,
	exports,
	MAX(exports) OVER ( PARTITION BY year)
FROM trades

-- which country had maximum export for each year

SELECT * FROM
(
SELECT
	country,
	year,
	RANK() OVER ( PARTITION BY year ORDER BY exports DESC) as exp_rank
FROM trades
) AS T
WHERE T.exp_rank = 1

-- NTILE()
-- ntile WILL SPLIT DATA IDEALLY INTO EQUAL GROUPS
-- divides ordered rows in the partition into a specified number of ranked buckets
-- bukcet number for each row starts with 1
-- If the number of rows is not divisible by the buckets, function return groups of two sizes
--  with difference of one

-- Get USA exports from year 2000 into 4 buckets

SELECT
	year,
	exports,
	NTILE(4) OVER (ORDER BY exports)
FROM trades
WHERE country = 'USA' AND year > 2000

-- LEAD & LAG

-- LEAD & LAG functions allows you to move lines within the resultsets
-- Very useful function to compare data of CURRENT ROW with any other rows
-- going backward is LAG and going forward is LEAD
-- LEAD/LAG (expression, offset, [default_value])

-- Calculate difference of exports from one year to another year for Belgium
SELECT
	country,
	exports AS exp,
	COALESCE(exp_nxt_yr, 0.0) AS exp_nxt,
	T.exp_nxt_yr - T.exports AS exp_diff
FROM
(SELECT
	country,
	year,
	exports,
	LEAD(exports, 1) OVER (ORDER BY year) AS exp_nxt_yr
FROM trades
WHERE country = 'Belgium') AS T

-- GET YEARS FOR ALL COUNTRIES WHERE THE DIFF B/W exports of cur yr and nxt yr was the most

SELECT
	country, max(export_diff)
FROM (
		SELECT
			country, year,
			exports - export_nxt AS export_diff
		FROM (
				SELECT
					country,
					year,
					exports,
					LEAD(exports, 1) OVER (PARTITION BY country ORDER BY year ASC) AS export_nxt
				FROM trades
			)
		)
group by country

-- above query works for countries but cannot give the year
--  if year is included in the query it gives all rows in the result

SELECT
	country, max(export_diff)
FROM (
		SELECT
			country, max(export_diff)
		FROM (
				SELECT
					country,
					year,
					exports - LEAD(exports, 1) OVER (PARTITION BY country ORDER BY year ASC) AS export_diff
				FROM trades
			)
			group by country
		)
group by country

WITH YearlyDiffs AS (
    SELECT
        country,
        year,
        exports - LEAD(exports) OVER (PARTITION BY country ORDER BY year ASC) AS export_diff
    FROM trades
),
RankedDiffs AS (
    SELECT
        country,
        year,
        export_diff,
        RANK() OVER (PARTITION BY country ORDER BY ABS(export_diff) DESC) as rnk
    FROM YearlyDiffs
    WHERE export_diff IS NOT NULL -- Excludes the last year since there's no "next" year
)
SELECT
    country,
    year,
    export_diff
FROM RankedDiffs
WHERE rnk = 1;

-- FIRST_VALUE() - returns the FIRST value of a sorted partition in a resultset
-- LAST_VALUE() - returns the LAST value of a sorted partition in a resultset
-- NTH_VALUE() - returns the value from the NTH row of a result set

SELECT
	year,
	imports,
	LAST_VALUE(imports) OVER (ORDER BY year UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
FROM trades
WHERE country = 'USA'

--  COrrelation

SELECT
	country,
	corr(imports, exports)
FROM trades
WHERE country IN ('USA', 'France', 'Japan', 'Brazil', 'Singapore')
GROUP BY country
ORDER BY 2 DESC
NULLS LAST

-- ROW_NUMBER() - assigns a unique integer value to each row in a result set starting with 1

-- Assign rows to all imports of FRance

SELECT
	year,
	imports,
	ROW_NUMBER() OVER (ORDER BY imports DESC)
FROM trades
WHERE
country = 'France'

-- Get 4th import for each country by year

SELECT * FROM (
SELECT
	country,
	year,
	imports,
	ROW_NUMBER() OVER (PARTITION BY country ORDER BY year) AS row_num
FROM trades ) AS T
WHERE row_num = 4
ORDER BY imports DESC

SELECT
	*
FROM trades

-- Orders shipping to USA or France
SELECT * FROM orders
WHERE ship_country IN ('USA', 'France')
ORDER BY ship_country

-- TOtal number of orders shipped to USA or FRance

SELECT ship_country, COUNT(*) FROM orders
WHERE ship_country IN ('USA', 'France')
GROUP BY ship_country
ORDER BY ship_country

-- Orders shipped to latin america

SELECT ship_country, COUNT(*) FROM orders
WHERE ship_country IN ('Brazil', 'Mexico', 'Argentina', 'Venezula')
GROUP BY ship_country
ORDER BY ship_country

-- SHow order total amount per each order line

SELECT
	order_id,
	product_id,
	((unit_price * quantity) -  discount) AS Total_amount
FROM order_details

-- FInd the latest and oldest order

SELECT
	MIN(order_date) as oldest_order,
	MAX(order_date) as latest_order
FROM orders

-- Total products in each category

SELECT
	COUNT(*) AS Count,
	c.category_name AS Category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
GROUP BY category_name

-- list products that need re-ordering

SELECT
	product_name
FROM products
WHERE units_in_stock <= reorder_level

-- List top 5 highest freight charges

SELECT
	ship_country,
	MAX(freight)
FROM orders
GROUP BY ship_country
ORDER BY 2 DESC
LIMIT 5

-- List top 5 highest freight charges for the year 1997

SELECT
	ship_country,
	MAX(freight)
FROM orders
WHERE order_date BETWEEN ('1997-01-01') AND ('1997-12-31')
GROUP BY ship_country
ORDER BY 2 DESC
LIMIT 5

-- List top 5 highest freight charges for last year

SELECT
	ship_country,
	MAX(freight)
FROM orders
WHERE EXTRACT('Y' FROM order_date) = EXTRACT('Y' FROM (SELECT MAX(order_date) FROM orders))
GROUP BY ship_country
ORDER BY 2 DESC
LIMIT 5

-- Customers with no orders

SELECT
	*
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
WHERE o.customer_id IS NULL

-- Top customers with their total order amount spend

SELECT
	c.customer_id,
	c.company_name,
	SUM((od.unit_rice * od.quantity) - od.discount) as total_amount
FROM customers c
INNER JOIN orders o ON o.customer_id = c.customer_id
JOIN order_details od ON od.order_id = o.order_id
GROUP BY c.customer_id, c.company_name

-- Orders with many lines of ordered items

SELECT
	order_id,
	COUNT(*)
FROM order_details
GROUP BY order_id
ORDER BY 2 DESC

-- Orders with double entry line items

SELECT
	order_id,
	quantity
FROM order_details
WHERE quantity > 60
GROUP BY
	order_id,
	quantity
HAVING
	COUNT(*) > 1
ORDER BY
	order_id

-- List all late shipped orders

SELECT
	*
FROM orders
WHERE
	shipped_date > required_date

-- List employees with late shipped orders

SELECT
	*
FROM orders

WITH late_orders AS (
	SELECT
		employee_id,
		COUNT(*) AS total_late_orders
	FROM orders
	WHERE
		shipped_date > required_date
	GROUP BY
		employee_id
),
all_orders AS (
	SELECT
		employee_id,
		COUNT(*) AS total_orders
	FROM orders
	GROUP BY
		employee_id
)
SELECT
	employees.first_name,
	employees.employee_id,
	all_orders.total_orders,
	late_orders.total_late_orders
FROM employees
JOIN all_orders ON all_orders.employee_id = employees.employee_id
JOIN late_orders ON late_orders.employee_id = employees.employee_id

-- Countries with customers or suppliers

SELECT
	country
FROM customers
UNION -- automatically removes duplicate rows
SELECT
	country
FROM suppliers
ORDER BY country

SELECT
	DISTINCT country
FROM customers
UNION ALL -- faster since it performs no data validation
SELECT
	DISTINCT country
FROM suppliers
ORDER BY country

-- Customers with multiple orders ( within 4 days)

WITH next_order_date AS (
	SELECT
		customer_id,
		order_date,
		LEAD(order_date, 1) OVER ( PARTITION BY customer_id ORDER BY customer_id, order_date) as next_order_date
	FROM orders
)
SELECT
	customer_id,
	order_date,
	next_order_date,
	(next_order_date - order_date) AS days_between_orders
FROM next_order_date
WHERE
	(next_order_date - order_date) <= 4

-- First order from each country

WITH orders_by_country AS (
	SELECT
		ship_country,
		order_id,
		order_date,
		ROW_NUMBER()
OVER (PARTITION BY ship_country ORDER BY ship_country, order_date) country_row_num
	FROM orders
)
SELECT
	ship_country,
	order_id,
	order_date
FROM orders_by_country
WHERE
	country_row_num = 1
ORDER BY
	ship_country