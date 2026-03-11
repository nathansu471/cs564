SELECT COUNT(DISTINCT(Users.UserID))
FROM Items JOIN Users ON Items.UserID = Users.UserID
WHERE Users.Rating > 1000