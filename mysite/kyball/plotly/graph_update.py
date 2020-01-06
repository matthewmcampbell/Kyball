import pandas as pd
import mysql.connector
import csv
import sys

def make_connection(host, user, passwd, database):
	connection = mysql.connector.connect(
	    host = host,
	    user = user,
	    passwd = passwd,
	    database = database
	)
	mycursor = connection.cursor(buffered=True)
	return (connection, mycursor)

def query(nameFirst, nameLast, cursor):
	capital = lambda x: x[0].upper() + x[1:]
	nameFirst = capital(nameFirst.strip())
	nameLast = capital(nameLast.strip())
	cursor.execute("SELECT * FROM People where nameFirst='%s' AND nameLast='%s'" % (nameFirst, nameLast))
	player = cursor.fetchone()
	if player == None:
		return None
	playerID = player[1]
	cursor.execute("SELECT * FROM Batting where playerID='%s'" % (playerID))
	batting_record = cursor.fetchall()
	return(batting_record)

def get_headers(tbl_name, cursor):
	cursor.execute("SHOW COLUMNS FROM %s" % tbl_name)
	cols = cursor.fetchall()
	return [data[0] for data in cols]

def update_graph_info(name, cursor):
	name = name.strip()
	names = name.split()
	if len(names) != 2:
		raise ValueError("Names aren't formatted well.")
	sql_data = query(names[0], names[1], cursor)
	headers = get_headers("Batting", cursor)
	df = pd.DataFrame(sql_data, columns=headers)
	traces = []
	traces.append(dict(
		x=df['yearID'],
		y=df['R'],
		mode='lines+markers',
		opacity=0.7,
		marker={
		    'size': 15,
		    'line': {'width': 0.5, 'color': 'white'}
		},
		name=name
	))

	return {
		'data': traces,
		'layout': dict(
		    title=name,
		    xaxis={'type': 'linear', 'title': 'Year',
				'range':[min(df['yearID'])-5, max(df['yearID'])+5]},
		    yaxis={'title': 'Runs', 'range': [min(df['R'])-5, max(df['R'])+5]},
		    margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
		    legend={'x': 0, 'y': 1},
		    hovermode='closest',
		    transition = {'duration': 500},
		)
	}

if __name__ == '__main__':
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