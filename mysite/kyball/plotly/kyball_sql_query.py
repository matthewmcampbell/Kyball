import mysql.connector
import csv
import sys
import pandas as pd

host = "kyball-mysql.cjgpo2iwqpsx.us-east-1.rds.amazonaws.com"
user = "kylexi"
passwd = "Nine9clock!"
database = "Kyball_db"

connection = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
    database = database
)
mycursor = connection.cursor(buffered=True)

def query(nameFirst, nameLast, cursor=mycursor):
	capital = lambda x: x[0].upper() + x[1:]
	nameFirst = capital(nameFirst.strip())
	nameLast = capital(nameLast.strip())
	mycursor.execute("SELECT * FROM People where nameFirst='%s' AND nameLast='%s'" % (nameLast, nameFirst))
	player = mycursor.fetchone()
	if player == None:
		return None
	playerID = player[1]
	mycursor.execute("SELECT * FROM Batting where playerID='%s'" % (playerID))
	batting_record = mycursor.fetchall()
	return(batting_record)

def get_headers(tbl_name, cursor=mycursor):
	mycursor.execute("SHOW COLUMNS FROM %s" % tbl_name)
	cols = mycursor.fetchall()
	return [data[0] for data in cols]