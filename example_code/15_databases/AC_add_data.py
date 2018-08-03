import sqlite3

conn = sqlite3.connect('AA_db.sqlite')
cur = conn.cursor()

cur.execute('INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description")')
conn.commit()

cur.execute('INSERT INTO experiments (name, description) VALUES (?, ?)',
            ('Another User', 'Another Experiment'))
conn.commit()

conn.close()