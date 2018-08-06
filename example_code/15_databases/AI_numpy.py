"""https://stackoverflow.com/a/18622264/4467480"""

import sqlite3
import numpy as np
import io

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)


conn = sqlite3.connect('AI_db.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cur = conn.cursor()
sql_command = """DROP TABLE IF EXISTS measurements;
CREATE TABLE measurements (
    id INTEGER PRIMARY KEY,
    description VARCHAR ,
    arr array);
"""
cur.executescript(sql_command)
conn.commit()



x = np.random.rand(10,2)

cur.execute('INSERT INTO measurements (arr) values (?)', (x,))

cur.execute('SELECT arr FROM measurements')
data = cur.fetchone()
conn.close()
print(data)