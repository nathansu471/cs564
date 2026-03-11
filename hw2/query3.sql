SELECT COUNT(*)
FROM (
  SELECT COUNT(*) as Number
  FROM Category
  GROUP BY ItemID
) AS subquery WHERE Number = 4