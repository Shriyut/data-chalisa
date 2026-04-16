-- https://datalemur.com/questions/click-through-rate

--Assume you have an events table on Facebook app analytics. Write a query to calculate the click-through rate (CTR) for the app in 2022 and round the results to 2 decimal places.
--
--Definition and note:
--
--Percentage of click-through rate (CTR) = 100.0 * Number of clicks / Number of impressions
--To avoid integer division, multiply the CTR by 100.0, not 100.
--events Table:
--Column Name	Type
--app_id	integer
--event_type	string
--timestamp	datetime
--events Example Input:
--app_id	event_type	timestamp
--123	impression	07/18/2022 11:36:12
--123	impression	07/18/2022 11:37:12
--123	click	07/18/2022 11:37:42
--234	impression	07/18/2022 14:15:12
--234	click	07/18/2022 14:16:12
--Example Output:
--app_id	ctr
--123	50.00
--234	100.00

WITH imp AS (
  SELECT app_id, COUNT(*) AS count
  FROM events
  WHERE event_type = 'impression'
    AND timestamp >= '2022-01-01' AND timestamp < '2023-01-01'
  GROUP BY app_id
),
clk AS (
  SELECT app_id, COUNT(*) AS count
  FROM events
  WHERE event_type = 'click'
    AND timestamp >= '2022-01-01' AND timestamp < '2023-01-01'
  GROUP BY app_id
)
SELECT i.app_id,
       ROUND(100.0 * c.count / i.count, 2) AS ctr
FROM imp i
INNER JOIN clk c ON c.app_id = i.app_id
ORDER BY app_id;

-- two full table scans not good for table with more than a billion rows

SELECT
  app_id,
  ROUND(
    100.0 * SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) /
            SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END),
    2
  ) AS ctr
FROM events
WHERE event_type IN ('impression', 'click')
  AND timestamp >= '2022-01-01'
  AND timestamp < '2023-01-01'
GROUP BY app_id
HAVING SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END) > 0
ORDER BY app_id;