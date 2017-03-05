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
    cursor = cnx.cursor()

    query = """CREATE TABLE Product
                (
                PersonID int,
                LastName varchar(255),
                FirstName varchar(255),
                Address varchar(255),
                City varchar(255)
                );
            """

    cursor.execute(query)
    cnx.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Database Up !")
    cnx.close()
