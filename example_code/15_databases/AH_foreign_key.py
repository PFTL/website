import sqlite3

conn = sqlite3.connect('AH_db.sqlite')
cur = conn.cursor()
sql_command = """DROP TABLE IF EXISTS experiments;
DROP TABLE IF EXISTS users;
CREATE TABLE  users(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id));
CREATE TABLE experiments (
    id INTEGER,
    user_id INTEGER NOT NULL , 
    description VARCHAR ,
    perfomed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
    FOREIGN KEY (user_id) REFERENCES users(id));
INSERT INTO users (name, email, phone) values ("Aquiles", "example@example.com", "123456789");
INSERT INTO experiments (user_id, description) values (1, "My experiment description");
INSERT INTO experiments (description) values ("My experiment description 2");
"""

cur.execute("PRAGMA foreign_keys = ON;")
cur.executescript(sql_command)
conn.commit()
cur.execute('SELECT * FROM experiments')
data = cur.fetchall()
cur.execute('SELECT * FROM users')
users = cur.fetchall()
conn.close()
print(30*'*' + 'Experiments' + 30*'*')
for d in data:
    print(d)
print(30*'*' + 'Users' + 30*'*')
for u in users:
    print(u)