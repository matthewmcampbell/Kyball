import pandas as pd
import mysql.connector
import csv
import sys
from .kyball_sql_query import query
from .kyball_sql_query import get_headers

def update_graph_info(name, cursor):
	name = name.strip()
	names = name.split()
	if len(names) != 2:
		raise ValueError("Names aren't formatted well.")
	sql_data = query(names[0], names[1], cursor)
	headers = get_headers("Batting")
	df = pd.DataFrame(sql_data, columns=headers)
	traces = []
	traces.append(dict(
		x=df['yearID'],
		y=df['R'],
		# text=df['country'],
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