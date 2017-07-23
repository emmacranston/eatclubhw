import pandas as pd

#converts MM/DD/YY dates to YYYY-MM-DD format for MySQL load
def date_convert(string):
	s = string
	vals = s.split("/")
	if len(str(vals[2])) == 2:
		y = str(vals[2])
	else:
		y = "0" + str(vals[2])

	if len(str(vals[0])) == 2:
		m = str(vals[0])
	else: 
		m = "0" + str(vals[0])

	if len(str(vals[1])) == 2:
		d = str(vals[1])
	else:
		d = "0" + str(vals[1])

	return "20%s-%s-%s" % (y, m, d)

#the Eat Club datetimes are improperly formatted for MySQL
def EC_datetime_convert(string):
	s = string
	split = s.split(" ")
	date = date_convert(split[0])

	t = split[1]
	if len(t) == 5:
		time = t + ":00"
	elif len(t) == 4:
		time = "0%s:00" % t
	else: time = "00:00:00"
	return date + " " + time

#now take the CSV files and convert to proper dates and datetimes
orders = pd.read_csv("/Users/emmacranston/Documents/analyst_homework/EatClub/PACS/orders.csv", sep=',', delimiter=None, header=0, index_col=0)
users = pd.read_csv("/Users/emmacranston/Documents/analyst_homework/EatClub/PACS/users.csv", sep=",", delimiter=None, header=0, index_col=0)
tags = pd.read_csv("/Users/emmacranston/Documents/analyst_homework/EatClub/PACS/tags.csv", sep=",", delimiter=None, header=0, index_col=0)

#convert dates and datetimes in Orders
orders['order_datetime'] = orders['order_datetime'].apply(lambda x: None if x == None else EC_datetime_convert(x))
orders['delivery_date'] = orders['delivery_date'].apply(lambda x: date_convert(x))

#convert dates in Users
users['joined_date'] = users['joined_date'].apply(lambda x: date_convert(x))

#convert value column in Tags to string
tags['value'] = tags['value'].apply(str)

#now write to CSV file
orders.to_csv("orders.csv")
users.to_csv("users.csv")
tags.to_csv("tags.csv")
