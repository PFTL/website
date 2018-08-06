import sqlite3

conn = sqlite3.connect('AH_db.sqlite')
cur = conn.cursor()

sql_command = """
SELECT users.id, users.name, experiments.description
FROM experiments
INNER JOIN users ON experiments.user_id=users.id
WHERE users.name="Aquiles";
"""
cur.execute(sql_command)
data = cur.fetchall()

for d in data:
    print(d)
