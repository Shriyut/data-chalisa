--https://leetcode.com/problems/average-selling-price/?envType=study-plan-v2&envId=top-sql-50

-- wrong answer ( 5 out of 17 test cases passed)
WITH data_rec AS
(SELECT p.product_id, avg(p.price*u.units) as total_price, u.units as units FROM Prices p
INNER JOIN UnitsSold u ON p.product_id = u.product_id WHERE u.purchase_date BETWEEN p.start_date AND p.end_date GROUP BY p.product_id, u.units)

SELECT distinct d1.product_id, round((d1.total_price + d2.total_price)/(d1.units + d2.units), 2) AS average_price FROM data_rec d1
LEFT JOIN data_rec d2
ON d1.product_id = d2.product_id AND d1.units != d2.units

--wrong answer (15 out of 17 test cases passed)
SELECT p.product_id, ROUND(SUM(units*price)/SUM(units)::numeric,2) AS average_price
FROM Prices p LEFT JOIN UnitsSold u
ON p.product_id = u.product_id AND
u.purchase_date BETWEEN start_date AND end_date
group by p.product_id

--correct answer
SELECT p.product_id,
CASE WHEN
ROUND(SUM(units*price)/SUM(units)::numeric,2) IS NULL THEN 0
ELSE ROUND(SUM(units*price)/SUM(units)::numeric,2) END AS average_price
FROM Prices p LEFT JOIN UnitsSold u
ON p.product_id = u.product_id AND
u.purchase_date BETWEEN start_date AND end_date
group by p.product_id


--little more optimizzed solution
select p.product_id, COALESCE(round(sum(p.price * u.units) / sum(u.units)::decimal, 2), 0) average_price
from prices p
left join unitssold u
on p.product_id = u.product_id
and u.purchase_date between start_date and end_date
group by p.product_id


