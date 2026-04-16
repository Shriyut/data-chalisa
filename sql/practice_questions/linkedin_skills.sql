-- https://datalemur.com/questions/matching-skills

SELECT candidate_id FROM (

SELECT candidate_id, COUNT(*) AS skill_count FROM candidates
WHERE skill IN ('Python', 'Tableau', 'PostgreSQL')
GROUP BY candidate_id
) t
WHERE t.skill_count = 3

-- more simplified approach to remove subquery mateerialization overhead

SELECT candidate_id
FROM candidates
WHERE skill IN ('Python', 'Tableau', 'PostgreSQL')
GROUP BY candidate_id
HAVING COUNT(DISTINCT skill) = 3;