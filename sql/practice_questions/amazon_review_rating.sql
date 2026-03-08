-- https://datalemur.com/questions/sql-avg-review-ratings

--Given the reviews table, write a query to retrieve the average star rating for each product, grouped by month.
--The output should display the month as a numerical value, product ID, and average star rating
--rounded to two decimal places. Sort the output first by month and then by product ID.

--
--reviews Table:
--Column Name	Type
--review_id	integer
--user_id	integer
--submit_date	datetime
--product_id	integer
--stars	integer (1-5)

--reviews Example Input:
--review_id	user_id	submit_date	product_id	stars
--6171	123	06/08/2022 00:00:00	50001	4
--7802	265	06/10/2022 00:00:00	69852	4
--5293	362	06/18/2022 00:00:00	50001	3
--6352	192	07/26/2022 00:00:00	69852	3
--4517	981	07/05/2022 00:00:00	69852	2


WITH reviews AS (
    SELECT
        stars,
        product_id,
        EXTRACT(MONTH FROM submit_date) AS mnth
    FROM reviews
)
SELECT mnth, product_id, ROUND(AVG(stars), 2) FROM reviews
GROUP BY product_id, mnth
ORDER BY mnth, product_id

-- NO need for temp table - created so that extract is only executed once

SELECT
  EXTRACT(MONTH FROM submit_date) AS mnth,
  product_id,
  ROUND(AVG(stars), 2) AS avg_Stars
FROM reviews
GROUP BY EXTRACT(MONTH FROM submit_date), product_id
ORDER BY EXTRACT(MONTH FROM submit_date), product_id