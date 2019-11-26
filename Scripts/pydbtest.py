import mysql.connector

connection = mysql.connector.connect(
	host = "testmysql.cjgpo2iwqpsx.us-east-1.rds.amazonaws.com",
	user = "kylexi",
	passwd = "Nine9clock!",
	database = "test_db"
)

mycursor = connection.cursor()

mycursor.execute("SHOW TABLES")
for x in mycursor:
	print(x)
input()


