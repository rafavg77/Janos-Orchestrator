# Creating table into database!!!
import sqlite3
import os

# Connect to sqlite database
conn = sqlite3.connect(os.environ.get('ORCHESTRATOR_DB'))
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

unique_hosts = """CREATE TABLE UNIQUE_HOSTS(
        ID INTEGER PRIMARY KEY,
        MAC CHAR(100) NOT NULL,
        HOSTNAME CHAR(100) NOT NULL,
        NOTIFY CHAR(10) NOT NULL, 
        DATE timestamp);"""

cursor.execute(unique_hosts)
conn.commit()

conn.close()