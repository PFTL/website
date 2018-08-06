import sqlite3

conn = sqlite3.connect('AF_db.sqlite')
cur = conn.cursor()
sql_command = """DROP TABLE IF EXISTS experiments;
CREATE TABLE experiments (
    id INTEGER,
    name VARCHAR(20) DEFAULT "Aquiles", 
    description VARCHAR ,
    perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id));
INSERT INTO experiments (description) values ("My experiment description");
INSERT INTO experiments (name, description) values ("Aquiles 2", "My experiment description 2");
"""

cur.executescript(sql_command)
conn.commit()
cur.execute('SELECT * FROM experiments WHERE id=1')
data = cur.fetchone()
conn.close()

print(data)