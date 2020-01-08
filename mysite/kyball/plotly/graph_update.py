import pandas as pd
import mysql.connector
import csv
import sys

def query_1(nameFirst, nameLast, cursor):
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

# print(query_1("Babe","Ruth",mycursor))

def query(nameFirst, nameLast, df_players, df_batting):
	capital = lambda x: x[0].upper() + x[1:]
	nameFirst = capital(nameFirst.strip())
	nameLast = capital(nameLast.strip())
	filtered_df = df_players[(df_players.nameFirst==nameFirst) & (df_players.nameLast==nameLast)]#cursor.execute("SELECT * FROM People where nameFirst='%s' AND nameLast='%s'" % (nameFirst, nameLast))
	playerID = filtered_df.playerID.iloc[0]
	# print((playerID, type(playerID), playerID.iloc[0]))
	batting_record = df_batting[df_batting.playerID==playerID]
	# cursor.execute("SELECT * FROM Batting where playerID='%s'" % (playerID))
	# batting_record = cursor.fetchall()
	return(batting_record)

def get_headers(tbl_name, cursor):
	cursor.execute("SHOW COLUMNS FROM %s" % tbl_name)
	cols = cursor.fetchall()
	return [data[0] for data in cols]

def initial_query(cursor):
	headers = get_headers("People", cursor)
	cursor.execute("SELECT * FROM People")
	df_people = pd.DataFrame(cursor.fetchall(), columns=headers)
	headers = get_headers("Batting", cursor)
	cursor.execute("SELECT * FROM Batting")
	df_batting = pd.DataFrame(cursor.fetchall(), columns=headers)
	return({"df_people": df_people, "df_batting": df_batting})

# dfs = initial_query(mycursor)
# print(query("Babe", "Ruth", dfs[0], dfs[1]))
def update_graph_info(name, dfs):
	name = name.strip()
	names = name.split()
	if len(names) != 2:
		raise ValueError("Names aren't formatted well.")
	df = query(names[0], names[1], dfs['df_people'], dfs['df_batting'])
	# headers = get_headers("Batting", cursor)
	# df = pd.DataFrame(sql_data, columns=headers)
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