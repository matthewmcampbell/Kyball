import mysql.connector
import pandas as pd
import csv

input_csv = "C:/cloud/Kyball/data_source/baseballdatabank-2019.2/core/Batting.csv"
host = "testmysql.cjgpo2iwqpsx.us-east-1.rds.amazonaws.com"
user = "kylexi"
passwd = "Nine9clock!"
database = "test_db"

connection = mysql.connector.connect(
	host = host,
	user = user,
	passwd = passwd,
	database = database
)
mycursor = connection.cursor(buffered=True)

def check_tbl_exists(tbl_name, create_tbl_str):
	try:
		mycursor.execute("""
			SELECT * FROM {} WHERE id=1
			""".format(tbl_name))
	except mysql.connector.errors.ProgrammingError as e:
		mycursor.execute(create_tbl_str)

# df = pd.read_csv("C:/cloud/Kyball/data_source/baseballdatabank-2019.2/core/Batting.csv")
# print(df)
# exit()
# df.to_sql()
people_tbl_str = """CREATE TABLE People (
	id INT NOT NULL AUTO_INCREMENT,
	playerID VARCHAR(30) NOT NULL,
	birthYear INT,
	birthMonth INT,
	birthDay INT,
	birthCountry VARCHAR(50),
	birthState VARCHAR(50),
	birthCity VARCHAR(50),
	deathYear INT,
	deathMonth INT,
	deathDay INT,
	deathCountry VARCHAR(50),
	deathState VARCHAR(50),
	deathCity VARCHAR(50),
	nameLast VARCHAR(50),
	nameFirst VARCHAR(50),
	nameGiven VARCHAR(100),
	weight INT,
	height INT,
	bats INT,
	throws INT,
	debut DATE,
	finalGame DATE,
	retroID VARCHAR(50),
	bbrefID VARCHAR(50),
	PRIMARY KEY (id)
	);"""

batting_tbl_str = """CREATE TABLE Batting (
	id INT NOT NULL AUTO_INCREMENT,
	playerID VARCHAR(30) NOT NULL,
	yearID INT,
	stint INT,
	teamID VARCHAR(10),
	lgID VARCHAR(10),
	G INT,
	AB INT,
	R INT,
	H INT,
	2B INT,
	3B INT,
	HR INT,
	RBI INT,
	SB INT,
	CS INT,
	BB INT,
	SO INT,
	IBB INT,
	HBP INT,
	SH INT,
	SF INT,
	GIDP INT,
	PRIMARY KEY (id)
	);"""

def pull_col_headers(tbl_str):
	list_by_commas = tbl_str.split(',')[1:-1]
	return(tuple(map(lambda x: x.split(' ')[0].strip(), list_by_commas)))

check_tbl_exists("People", people_tbl_str)
check_tbl_exists("Batting", batting_tbl_str)
mycursor.execute("SHOW TABLES;")

def write_data(tbl_name, tbl_str, path_to_csv):
	headers = pull_col_headers(tbl_str)
	data = csv.reader(open(path_to_csv,'r'))
	data = list(data)[1:]
	sql_headers = ''
	for header in headers:
		sql_headers += header + ', '
	sql_headers = sql_headers[:-2]
	data = list(map(lambda x: tuple(x), data))
	abstract_values = str(tuple(['%s']*len(headers)))
	sql_cmd = "INSERT INTO {} {} VALUES {};".format(tbl_name, data, abstract_values)
	print(data[1])
	for i in range(1, len(data)):
		print(sql_cmd, data[i])
		mycursor.execute(sql_cmd, data[i])
	exit()

write_data('Batting', batting_tbl_str, input_csv)