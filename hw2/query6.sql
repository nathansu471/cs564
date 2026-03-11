SELECT COUNT(DISTINCT(Users.UserID))
FROM Users 
JOIN Items ON Users.UserID = Items.UserID
JOIN Bids ON Users.UserID = Bids.UserID