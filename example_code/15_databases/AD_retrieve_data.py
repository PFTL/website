import sqlite3

conn = sqlite3.connect('AA_db.sqlite')
cur = conn.cursor()
cur.execute('SELECT * FROM experiments')
data = cur.fetchall()

cur.execute('SELECT * FROM experiments')
data_2 = cur.fetchone()

cur.execute('SELECT * FROM experiments WHERE name="Aquiles"')
data_3 = cur.fetchall()
conn.close()

print(data)
print(data_2)
print(data_3)

