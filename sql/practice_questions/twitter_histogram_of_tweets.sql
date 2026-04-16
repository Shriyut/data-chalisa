--https://datalemur.com/questions/sql-histogram-tweets

--Assume you're given a table Twitter tweet data, write a query to obtain a histogram of tweets posted per user in 2022. Output the tweet count per user as the bucket and the number of Twitter users who fall into that bucket.
--
--In other words, group the users by the number of tweets they posted in 2022 and count the number of users in each group.
--
--tweets Table:
--Column Name	Type
--tweet_id	integer
--user_id	integer
--msg	string
--tweet_date	timestamp
--tweets Example Input:
--tweet_id	user_id	msg	tweet_date
--214252	111	Am considering taking Tesla private at $420. Funding secured.	12/30/2021 00:00:00
--739252	111	Despite the constant negative press covfefe	01/01/2022 00:00:00
--846402	111	Following @NickSinghTech on Twitter changed my life!	02/14/2022 00:00:00
--241425	254	If the salary is so competitive why won’t you tell me what it is?	03/01/2022 00:00:00
--231574	148	I no longer have a manager. I can't be managed	03/23/2022 00:00:00
--Example Output:
--tweet_bucket	users_num
--1	2
--2	1

WITH data_s AS (
SELECT
  COUNT(*) AS tweet_bucket,
  user_id
FROM tweets
WHERE EXTRACT(YEAR FROM tweet_date) = '2022' -- implicit casting eeds to be performed better to use 2022 without quotes
GROUP BY user_id
)

SELECT
tweet_bucket,
COUNT(*) AS users_num
FROM data_s
GROUP BY tweet_bucket

-- more optimized approach

SELECT tweet_count AS tweet_bucket,
       COUNT(*)    AS users_num
FROM (
    SELECT user_id,
           COUNT(*) AS tweet_count
    FROM tweets
    WHERE tweet_date >= '2022-01-01'
      AND tweet_date  < '2023-01-01'
    GROUP BY user_id
) AS tweet_data
GROUP BY tweet_count
ORDER BY tweet_bucket;

-- Extract need sto be performed on each row and benefits of indexing would be ignored, range scan would only process 1 year of data

-- Try to solve this using joins