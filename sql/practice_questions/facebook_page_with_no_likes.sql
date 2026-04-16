-- https://datalemur.com/questions/sql-page-with-no-likes

--Assume you're given two tables containing data about Facebook Pages and their respective likes (as in "Like a Facebook Page").
--
--Write a query to return the IDs of the Facebook pages that have zero likes. The output should be sorted in ascending order based on the page IDs.
--
--pages Table:
--Column Name	Type
--page_id	integer
--page_name	varchar
--pages Example Input:
--page_id	page_name
--20001	SQL Solutions
--20045	Brain Exercises
--20701	Tips for Data Analysts
--page_likes Table:
--Column Name	Type
--user_id	integer
--page_id	integer
--liked_date	datetime
--page_likes Example Input:
--user_id	page_id	liked_date
--111	20001	04/08/2022 00:00:00
--121	20045	03/12/2022 00:00:00
--156	20001	07/25/2022 00:00:00
--Example Output:
--page_id
--20701

SELECT page_id FROM pages
WHERE page_id NOT IN (
  SELECT DISTINCT page_id FROM page_likes
)

--Performance Analysis at Scale (1 Billion+ Rows)
--🔴 Critical Issues
--IssueImpactNOT IN with NULLsIf even ONE page_id in page_likes is NULL, the entire query returns EMPTY result set. This is because NOT IN uses three-valued logic — x NOT IN (..., NULL, ...) evaluates to UNKNOWN, never TRUE.Materialization CostThe subquery result set is fully materialized in memory. With billions of likes, this intermediate result can be massive.O(n × m) ComparisonFor each page (n), the engine may do a linear scan of the subquery result (m). Without optimization, this is extremely expensive.DISTINCT OverheadRequires sorting or hashing the entire page_likes table to deduplicate — unnecessary overhead.
--🔴 NOT IN NULL Trap — Detailed Example
--Copypage_likes contains: [1, 2, NULL, 3]

-- For page_id = 5:
--5 NOT IN (1, 2, NULL, 3)
--= (5≠1) AND (5≠2) AND (5≠NULL) AND (5≠3)
--= TRUE AND TRUE AND UNKNOWN AND TRUE
--= UNKNOWN  ← NOT TRUE, so row is excluded!

-- Result: NO rows returned at all!

Better Alternatives
--✅ Option 1: NOT EXISTS (Recommended)
SELECT p.page_id
FROM pages p
WHERE NOT EXISTS (
  SELECT 1 FROM page_likes pl
  WHERE pl.page_id = p.page_id
)
--Why better:
--
--NULL-safe: NOT EXISTS returns TRUE/FALSE only — no three-valued logic problem
--Short-circuit evaluation: Stops scanning page_likes as soon as one match is found (doesn't need to find all matches)
--No materialization: Uses a correlated semi-anti-join — the optimizer converts this into an efficient join strategy
--No DISTINCT needed: Inherently checks for existence, not values

--✅ Option 2: LEFT JOIN / IS NULL (Anti-Join)
SELECT p.page_id
FROM pages p
LEFT JOIN page_likes pl ON p.page_id = pl.page_id
WHERE pl.page_id IS NULL
--Why better:
--
--Most query engines optimize this into a Hash Anti-Join or Merge Anti-Join
--Single pass through both tables
--Very efficient at scale
--
--
--BigQuery-Specific Considerations
--AspectDetailNOT INBigQuery fully materializes the subquery, which can cause memory pressure and shuffle overhead at billion-row scaleNOT EXISTSBigQuery's optimizer converts this to an efficient anti-join execution planLEFT JOIN + IS NULLAlso converted to anti-join; essentially equivalent to NOT EXISTS in BigQueryPartitioningIf page_likes is partitioned (e.g., by date), none of these queries benefit unless you add a partition filterClusteringClustering page_likes on page_id dramatically speeds up the join/lookup
--
--Execution Plan Comparison (Conceptual)
--CopyNOT IN:          pages ──► Full Scan ──► Compare against MATERIALIZED SET ──► Filter
--NOT EXISTS:      pages ──► Hash Anti-Join with page_likes ──► Output
--LEFT JOIN:       pages ──► Hash Anti-Join with page_likes ──► Output
--
--Verdict
--CriteriaNOT INNOT EXISTSLEFT JOINCorrectness (NULLs)❌ Dangerous✅ Safe✅ SafePerformance (1B rows)❌ Poor✅ Optimal✅ OptimalReadability✅ Simple✅ Clear✅ ClearRecommendationAvoidBest choiceEqually good
--
--Bottom Line: The given solution is functionally correct only if page_id in page_likes is guaranteed NOT NULL. At billion-row scale, always prefer NOT EXISTS — it's both NULL-safe and performance-optimal across BigQuery, Cloud SQL, and virtually every SQL engine.