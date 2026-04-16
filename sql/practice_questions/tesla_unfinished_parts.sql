-- https://datalemur.com/questions/tesla-unfinished-parts

--Tesla is investigating production bottlenecks and they need your help to extract the relevant data. Write a query to determine which parts have begun the assembly process but are not yet finished.
--
--Assumptions:
--
--parts_assembly table contains all parts currently in production, each at varying stages of the assembly process.
--An unfinished part is one that lacks a finish_date.
--This question is straightforward, so let's approach it with simplicity in both thinking and solution.
--
--Effective April 11th 2023, the problem statement and assumptions were updated to enhance clarity.
--
--parts_assembly Table
--Column Name	Type
--part	string
--finish_date	datetime
--assembly_step	integer
--parts_assembly Example Input
--part	finish_date	assembly_step
--battery	01/22/2022 00:00:00	1
--battery	02/22/2022 00:00:00	2
--battery	03/22/2022 00:00:00	3
--bumper	01/22/2022 00:00:00	1
--bumper	02/22/2022 00:00:00	2
--bumper		3
--bumper		4
--Example Output
--part	assembly_step
--bumper	3
--bumper	4

SELECT part, assembly_step FROM parts_assembly
WHERE finish_date IS NULL

--Performance Concerns at 1B+ Rows
--🔴 Problem: Full Table Scan
--With 1 billion+ rows and no index on finish_date, this query triggers a full table scan, which is extremely expensive.
--Optimizations
--1. Indexing (Cloud SQL / Traditional RDBMS)
-- Partial index (PostgreSQL) — only indexes NULL values
CREATE INDEX idx_unfinished_parts
ON parts_assembly(part, assembly_step)
WHERE finish_date IS NULL;
--
---- Regular index (MySQL/SQL Server)
CREATE INDEX idx_finish_date
ON parts_assembly(finish_date);
--A partial/filtered index is ideal here because we only care about NULL rows, which are likely a small subset of 1B+ rows.
--2. BigQuery Specific Optimizations
SELECT part, assembly_step
FROM parts_assembly
WHERE finish_date IS NULL
--
--BigQuery is columnar — it only reads the 3 columns (part, assembly_step, finish_date), not all columns. This is a natural advantage.
--Partitioning: If the table is partitioned by finish_date, NULL values go into a special __NULL__ partition, making this query extremely fast as it only scans that one partition.
--Clustering: Clustering by finish_date would physically co-locate NULL rows, reducing bytes scanned.