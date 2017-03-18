import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'user',
    'password': 'user',
    'host': 'mysql',
    'database': 'crawler',
    'raise_on_warnings': True,
}

try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)


cursor = cnx.cursor()

query_movie = ("SELECT id FROM movie WHERE imdb_id = %s")

try:
    cursor.execute(query_movie, ('azer',))
except mysql.connector.Error as err:
    print(err)

row = cursor.fetchone()
print(row)

if row is None:  # Add the movie if it doesn't exist
    query_add_movie = ("INSERT INTO movie (imdb_id, title, `year`) VALUES(%s, %s, %s)")

    try:
        cursor.execute(query_add_movie, ('azer', 'azer', 5244))
    except mysql.connector.Error as err:
        print(err)
    id = cursor.lastrowid
else:
    id = 'bbop'

print(id)
cursor.close()
cnx.close()