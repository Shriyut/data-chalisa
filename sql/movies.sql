SELECT
	CONCAT(d.first_name, d.last_name) AS "direcotr_name",
	COUNT(mv.movie_name) AS num_movies
FROM directors d
LEFT JOIN movies mv on d.director_id = mv.director_id
GROUP BY d.director_id
ORDER BY num_movies DESC

SELECT
	*
FROM directors
LEFT JOIN movies mv USING (director_id)

-- total revenue done by each film for each director
-- USING WINDOWING COMPARE THE DIFF IN DIRECOTRS OVERALL EARNIGN AND EARNIGN OF THE MOVIE
SELECT
	-- mv.movie_name,
	CONCAT(d.first_name, d.last_name) as director_name,
	SUM(mv_rev.revenues_domestic + mv_rev.revenues_international) AS total_REv
FROM directors d
RIGHT JOIN movies mv ON d.director_id = mv.director_id
LEFT JOIN movies_revenues mv_rev ON mv.movie_id = mv_rev.movie_id
-- GROUP BY d.director_id, mv.movie_name
GROUP BY d.director_id
HAVING SUM(mv_rev.revenues_domestic + mv_rev.revenues_international) > 100
ORDER BY 2 DESC NULLS LAST


SELECT
	-- d.first_name,
	CONCAT(d.first_name, d.last_name) AS dirctor_name,
	COUNT(*) AS num_movies
FROM directors d
RIGHT JOIN movies mv USING (director_id)
-- GROUP BY director_id
GROUP BY d.first_name, d.last_name
ORDER BY 2 DESC, d.first_name DESC

SELECT
	CONCAT(d.first_name, d.last_name) AS dirctr_name,
	-- mv.movie_name AS movie_name,
	-- mv_rev.revenues_domestic AS domestic_Rev,
	-- mv_rev.revenues_international AS international_Rev,
	sum(mv_rev.revenues_domestic + mv_rev.revenues_international) AS total_rev
FROM directors d
LEFT JOIN movies mv USING (director_id)
LEFT JOIN movies_revenues mv_rev USING (movie_id)
GROUP BY d.first_name, d.last_name
HAVING sum(mv_rev.revenues_domestic + mv_rev.revenues_international) > 0


SELECT
	mv.age_certificate,

	CONCAT(d.first_name, d.last_name) AS "dirctr_name",
	COUNT(*) AS num_movies
FROM directors d
LEFT JOIN movies mv USING (director_id)
WHERE d.nationality IN ('American', 'Chinese', 'Japanese')
GROUP BY d.director_id, mv.age_certificate
ORDER BY AGE_CERTIFICATE desc, DIRCTR_NAME DESC