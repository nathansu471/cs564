rm -r -f *.dat
rm -r -f *.db
python skeleton_parser.py ebay_data/items-*.json
sort -u category.dat -o category.dat
sort -u users.dat -o users.dat
sort -u bids.dat -o bids.dat
sort -u items.dat -o items.dat
sqlite3 ebayAuction.db < create.sql
sqlite3 ebayAuction.db < load.txt