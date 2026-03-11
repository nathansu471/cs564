SELECT COUNT(DISTINCT(Category.Category_Name))
FROM Category
JOIN Bids ON Category.ItemID = Bids.ItemID
WHERE Bids.Amount != "NULL" AND Bids.Amount > 100