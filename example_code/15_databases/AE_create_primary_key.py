import sqlite3

conn = sqlite3.connect('AA_db.sqlite')
cur = conn.cursor()
sql_command = """DROP TABLE IF EXISTS experiments;
CREATE TABLE experiments (
    id INTEGER,
    name STRING, 
    description STRING,
    PRIMARY KEY (id));
INSERT INTO experiments (name, description) values ("Aquiles", "My experiment description");
INSERT INTO experiments (name, description) values ("Aquiles 2", "My experiment description 2");
"""

cur.executescript(sql_command)
conn.commit()
cur.execute('SELECT * FROM experiments WHERE id=1')
data = cur.fetchone()
conn.close()

print(data)
