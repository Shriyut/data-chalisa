-- using case in where condition

--For Instagram, we're filtering actors with 500,000 or more followers.
--For Twitter, we're filtering actors with 200,000 or more followers.
--For other platforms, we're filtering actors with 100,000 or more followers.

SELECT
  actor,
  character,
  platform
FROM marvel_avengers
WHERE
  CASE
    WHEN platform = 'Instagram' THEN followers >= 500000
    WHEN platform = 'Twitter' THEN followers >= 200000
    ELSE followers >= 100000
  END;

