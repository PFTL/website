import sqlite3

conn = sqlite3.connect('AA_db.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE experiments (name VARCHAR, description VARCHAR)')
conn.commit()

conn.close()