import sqlite3

conn = sqlite3.connect('AG_db.sqlite')
cur = conn.cursor()
sql_command = """DROP TABLE IF EXISTS experiments;
CREATE TABLE experiments (
    id INTEGER,
    name VARCHAR DEFAULT "Aquiles", 
    description VARCHAR ,
    perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    value INTEGER DEFAULT 0,
    PRIMARY KEY (id));
INSERT INTO experiments (description) values ("My experiment description");
INSERT INTO experiments (name, description) values ("Aquiles Very Long Name", "My experiment description 2");
INSERT INTO experiments (name, description, value) values ("Aquiles Very Long Name", "My experiment description 2", 1000);
"""

cur.executescript(sql_command)
conn.commit()
cur.execute('SELECT * FROM experiments')
data = cur.fetchall()
conn.close()

for d in data:
    print(d)
