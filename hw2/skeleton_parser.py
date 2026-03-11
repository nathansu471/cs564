
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        category_file = open("category.dat", "a")
        items_file = open("items.dat", "a")
        bids_file = open("bids.dat", "a")
        users_file = open("users.dat", "a")

        written_users = set()

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            # items
            # Items(ItemID, UserID, Name, Category, Currently, Buy_Price, First_Bid, Number_of_Bids, Started, Ends, Description)
            items_line = []
            itemID = item["ItemID"]
            if itemID == None:
                itemID = "NULL"
            items_line.append(itemID)

            if item["Seller"]["UserID"] == None:
                items_line.append("NULL")
            else:
                userID = '"' + sub('"', '""', item["Seller"]["UserID"]) + '"'
                items_line.append(userID)

            if item["Name"] == None:
                items_line.append("NULL")
            else:
                name = '"' + sub('"', '""', item["Name"]) + '"'
                items_line.append(name)

            if item["Currently"] == None:
                items_line.append("NULL")
            else:             
                 currently = transformDollar(str(item["Currently"]))
                 items_line.append(currently)

            if "Buy_Price" not in item or item["Buy_Price"] == None:
                items_line.append("NULL")
            else:
                buy_price = transformDollar(str(item["Buy_Price"]))
                items_line.append(buy_price)

            if item["First_Bid"] == None:
                items_line.append("NULL")
            else:
                first_bid = transformDollar(str(item["First_Bid"]))
                items_line.append(first_bid)

            if item["Number_of_Bids"] == None:
                items_line.append("NULL")
            else:
                number_of_bids = str(item["Number_of_Bids"])
                items_line.append(number_of_bids)

            if item["Started"] == None:
                items_line.append("NULL")
            else:
                started = transformDttm(str(item["Started"]))
                items_line.append(started)

            if item["Ends"] == None:
                items_line.append("NULL")
            else:
                ends = transformDttm(str(item["Ends"]))
                items_line.append(ends)

            if item["Description"] == None:
                items_line.append("NULL")
            else:
                description = '"' + sub('"', '""', item["Description"]) + '"'
                items_line.append(description)

            items_file.write("|".join(items_line) + "\n")

            # category
            # Category(Category_Name, ItemID)
            for category in item["Category"]:
                category_line = ['"' + sub('"', '""', category) + '"', itemID]
                category_file.write("|".join(category_line) + "\n")

            # bids
            #Bids(BidID, UserID, Time, Amount)
            if "Bids" not in item or item["Bids"] == None:
                bids_file.write(itemID + "|" + "NULL" + "|" + "NULL" + "|" + "NULL" + "\n")
            else:
                for bid in item["Bids"]:
                    bid_line = []

                    if itemID == None:
                        bid_line.append("NULL")
                    else:
                        bid_line.append(itemID)

                    if bid["Bid"]["Bidder"]["UserID"] == None:
                        bid_line.append("NULL")
                    else:
                        userID = '"' + sub('"', '""', bid["Bid"]["Bidder"]["UserID"]) + '"'
                        bid_line.append(userID)

                    if bid["Bid"]["Time"] == None:
                        bid_line.append("NULL")
                    else:
                        time = transformDttm(str(bid["Bid"]["Time"]))
                        bid_line.append(time)

                    if bid["Bid"]["Amount"] == None:
                        bid_line.append("NULL")
                    else:
                        amount = transformDollar(str(bid["Bid"]["Amount"]))
                        bid_line.append(amount)

                    bids_file.write("|".join(bid_line) + "\n")

                    
            
            # users
            # User(UserID, Location, Country, Rating)
            # sellers
            if "Seller" in item and item["Seller"] != None and item["Seller"]["UserID"] not in written_users:
                user_line = []
                if "UserID" in item["Seller"] and item["Seller"]["UserID"] != None:
                    userID = '"' + sub('"', '""', item["Seller"]["UserID"]) + '"'
                    user_line.append(userID)
                else:
                    user_line.append("NULL")

                if "Location" in item and item["Location"] != None:
                    location = '"' + sub('"', '""', item["Location"]) + '"'
                    user_line.append(location)
                else:
                    user_line.append("NULL")

                if "Country" in item and item["Country"] != None:
                    country = '"' + sub('"', '""', item["Country"]) + '"'
                    user_line.append(country)
                else:
                    user_line.append("NULL")

                if "Rating" in item["Seller"] and item["Seller"]["Rating"] != None:
                    rating = str(item["Seller"]["Rating"])
                    user_line.append(rating)
                else:
                    user_line.append("NULL")

                users_file.write("|".join(user_line) + "\n")
                written_users.add(item["Seller"]["UserID"])

            # bidders
            if "Bids" in item and item["Bids"] != None:
                for bid in item["Bids"]:
                    bidder = bid["Bid"]["Bidder"]

                    userID_raw = bidder.get("UserID", None)
                    if userID_raw is None or userID_raw in written_users:
                        continue

                    user_line = []

                    if "UserID" in bidder and bidder["UserID"] != None:
                        userID = '"' + sub('"', '""', bidder["UserID"]) + '"'
                        user_line.append(userID)
                    else:
                        user_line.append("NULL")

                    if "Location" in bidder and bidder["Location"] != None:
                        location = '"' + sub('"', '""', bidder["Location"]) + '"'
                        user_line.append(location)
                    else:
                        user_line.append("NULL")

                    if "Country" in bidder and bidder["Country"] != None:
                        country = '"' + sub('"', '""', bidder["Country"]) + '"'
                        user_line.append(country)
                    else:
                        user_line.append("NULL")

                    if "Rating" in bidder and bidder["Rating"] != None:
                        rating = str(bidder["Rating"])
                        user_line.append(rating)
                    else:
                        user_line.append("NULL")

                    users_file.write("|".join(user_line) + "\n")
                    written_users.add(bidder["UserID"])


        category_file.close()
        items_file.close()
        bids_file.close()
        users_file.close()


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
