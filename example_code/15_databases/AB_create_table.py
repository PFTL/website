import sqlite3

conn = sqlite3.connect('AA_db.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE experiments (name STRING, description STRING)')
conn.commit()

conn.close()