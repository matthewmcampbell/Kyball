import mysql.connector
import csv
import sys

if len(sys.argv) != 5:
	raise ValueError('''Not enough input paramaters to write to MySQL.
		Check user data or write_to_sql_from_ec2.py''')
input_csv = "/home/ec2-user/Projects/Kyball/data_source/baseballdatabank-2019.2/core/"
host = sys.argv[1] #"testmysql.cjgpo2iwqpsx.us-east-1.rds.amazonaws.com"
database = sys.argv[2] #"Kyball_db"
user = sys.argv[3] #"kylexi"
passwd = sys.argv[4] #"Nine9clock!"

connection = mysql.connector.connect(
	host = host,
	user = user,
	passwd = passwd,
	# database = database
)
mycursor = connection.cursor(buffered=True)

def make_db_and_switch(db_name):
	try:
		mycursor.execute('CREATE DATABASE {}'.format(db_name))
		mycursor.execute('USE {}'.format(db_name))
	except:
		mycursor.execute('USE {}'.format(db_name))

def check_tbl_exists(tbl_name, create_tbl_str):
	try:
		mycursor.execute("""
			SELECT * FROM {} WHERE id=1
			""".format(tbl_name))
	except mysql.connector.errors.ProgrammingError as e:
		mycursor.execute(create_tbl_str)

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
	headers = tuple(map(lambda x: x.split(' ')[0].strip(), list_by_commas))
	header_as_string = ''
	for header in headers:
		header_as_string += header + ', '
	return header_as_string[:-2]

def write_data(tbl_name, tbl_str, path_to_csv):
	path_to_csv += tbl_name + '.csv' #update path to specific csv
	headers = pull_col_headers(tbl_str)
	data = csv.reader(open(path_to_csv,'r'))
	data = list(data)[1:]
	data = list(map(lambda x: tuple(x), data))
	abstract_values = '%s, ' * len(headers.split(','))
	abstract_values = abstract_values[:-2]
	for i in range(1, len(data)):
		sql_cmd = "INSERT INTO {} ({}) VALUES ({});".format(tbl_name, headers, abstract_values)
		mycursor.execute(sql_cmd, data[i])
		print(i)
	connection.commit()

def main():
	make_db_and_switch(database)

	check_tbl_exists("People", people_tbl_str)
	check_tbl_exists("Batting", batting_tbl_str)
	mycursor.execute("SHOW TABLES;")

	write_data('People', people_tbl_str, input_csv)
	write_data('Batting', batting_tbl_str, input_csv)

if __name__ == '__main__':
	main()