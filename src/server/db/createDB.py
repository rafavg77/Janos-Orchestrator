# Creating table into database!!!
import sqlite3
# Connect to sqlite database
conn = sqlite3.connect('hosts.db')
# cursor object
cursor = conn.cursor()
# drop query
cursor.execute("DROP TABLE IF EXISTS HOSTS")
# create query
query = """CREATE TABLE HOSTS(
        ID INTEGER PRIMARY KEY,
        IP CHAR(100) NOT NULL,
        MAC CHAR(100) NOT NULL,
        HOSTNAME CHAR(100) NOT NULL, 
        DATE timestamp);"""

cursor.execute(query)
# commit and close
conn.commit()
conn.close()