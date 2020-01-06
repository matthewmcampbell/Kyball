# import plotly.kyball_sql_query as # import plotly.graph_update as gu
from .plotly.graph_update import update_graph_info, make_connection, query, get_headers
import mysql.connector
import os
'''
Testing
'''
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'db_access_info.txt')

try:
    file   = list(open(filename, 'r').readlines())
    host   = file[0].strip()
    user   = file[1].strip()
    passwd = file[2].strip()
except:
    host = None
    user = None
    passwd = None

database = "Kyball_db"

def test_connection():
	print(file.readlines(), host, user, passwd, database)
	connection, cursor = make_connection(host, user, passwd, database)
	assert(type(cursor) == mysql.connector.cursor_cext.CMySQLCursorBuffered)

def test_bad_query_1():
	# Doesn't meet the min len requirements on the names
	connection, cursor = make_connection(host, user, passwd, database)
	assert(query("A", "A", cursor) == None)

def test_non_existent_player():
	# Name doesn't come up in db
	connection, cursor = make_connection(host, user, passwd, database)
	assert(query("Joe", "Laman", cursor) == None)

def test_babe_ruth():
	connection, cursor = make_connection(host, user, passwd, database)
	assert(query("Babe", "Ruth", cursor) == [(15064, 'ruthba01', 1914, 1, 'BOS', 'AL', 5, 10, 1, 2, 1, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0), (15849, 'ruthba01', 1915, 1, 'BOS', 'AL', 42, 92, 16, 29, 10, 1, 4, 21, 0, 0, 9, 23, 0, 0, 2, 0, 0), (16470, 'ruthba01', 1916, 1, 'BOS', 'AL', 67, 136, 18, 37, 5, 3, 3, 15, 0, 0, 10, 23, 0, 0, 4, 0, 0), (16991, 'ruthba01', 1917, 1, 'BOS', 'AL', 52, 123, 14, 40, 6, 3, 2, 12, 0, 0, 12, 18, 0, 0, 7, 0, 0), (17505, 'ruthba01', 1918, 1, 'BOS', 'AL', 95, 317, 50, 95, 26, 11, 11, 66, 6, 0, 58, 58, 0, 2, 3, 0, 0), (18017, 'ruthba01', 1919, 1, 'BOS', 'AL', 130, 432, 103, 139, 34, 12, 29, 114, 7, 0, 101, 58, 0, 6, 3, 0, 0), (18534, 'ruthba01', 1920, 1, 'NYA', 'AL', 142, 457, 158, 172, 36, 9, 54, 137, 14, 14, 150, 80, 0, 3, 5, 0, 0), (19054, 'ruthba01', 1921, 1, 'NYA', 'AL', 152, 540, 177, 204, 44, 16, 59, 171, 17, 13, 145, 81, 0, 4, 4, 0, 0), (19588, 'ruthba01', 1922, 1, 'NYA', 'AL', 110, 406, 94, 128, 24, 8, 35, 99, 2, 5, 84, 80, 0, 1, 4, 0, 0), (20111, 'ruthba01', 1923, 1, 'NYA', 'AL', 152, 522, 151, 205, 45, 13, 41, 131, 17, 21, 170, 93, 0, 4, 3, 0, 0), (20651, 'ruthba01', 1924, 1, 'NYA', 'AL', 153, 529, 143, 200, 39, 7, 46, 121, 9, 13, 142, 81, 0, 4, 6, 0, 0), (21203, 'ruthba01', 1925, 1, 'NYA', 'AL', 98, 359, 61, 104, 12, 2, 25, 66, 2, 4, 59, 68, 0, 2, 6, 0, 0), (21733, 'ruthba01', 1926, 1, 'NYA', 'AL', 152, 495, 139, 184, 30, 5, 47, 150, 11, 9, 144, 76, 0, 3, 10, 0, 0), (22271, 'ruthba01', 1927, 1, 'NYA', 'AL', 151, 540, 158, 192, 29, 8, 60, 164, 7, 6, 137, 89, 0, 0, 14, 0, 0), (22801, 'ruthba01', 1928, 1, 'NYA', 'AL', 154, 536, 163, 173, 29, 8, 54, 142, 4, 5, 137, 87, 0, 3, 8, 0, 0), (23345, 'ruthba01', 1929, 1, 'NYA', 'AL', 135, 499, 121, 172, 26, 6, 46, 154, 5, 3, 72, 60, 0, 3, 13, 0, 0), (23877, 'ruthba01', 1930, 1, 'NYA', 'AL', 145, 518, 150, 186, 28, 9, 49, 153, 10, 10, 136, 61, 0, 1, 21, 0, 0), (24382, 'ruthba01', 1931, 1, 'NYA', 'AL', 145, 534, 149, 199, 31, 3, 46, 163, 5, 4, 128, 51, 0, 1, 0, 0, 0), (24911, 'ruthba01', 1932, 1, 'NYA', 'AL', 133, 457, 120, 156, 13, 5, 41, 137, 2, 2, 130, 62, 0, 2, 0, 0, 0), (25408, 'ruthba01', 1933, 1, 'NYA', 'AL', 137, 459, 97, 138, 21, 3, 34, 103, 4, 5, 114, 90, 0, 2, 0, 0, 0), (25922, 'ruthba01', 1934, 1, 'NYA', 'AL', 125, 365, 78, 105, 17, 4, 22, 84, 1, 3, 104, 63, 0, 2, 0, 0, 0), (26436, 'ruthba01', 1935, 1, 'BSN', 'NL', 28, 72, 13, 13, 0, 0, 6, 12, 0, 0, 20, 24, 0, 0, 0, 0, 2)])
