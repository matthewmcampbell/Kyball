import os
import mysql.connector

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

try:
    connection = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
        database = database
    )
    mycursor = connection.cursor(buffered=True)
except:
    mycursor = None

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

print(query("Babe", "Ruth", mycursor))