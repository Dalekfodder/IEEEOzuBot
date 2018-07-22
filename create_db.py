import sqlite3

conn = sqlite3.connect("cevap.db")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE answers (id INTEGER PRIMARY KEY, tags, cevap)''')
cursor.execute('''INSERT INTO answers VALUES (0, 'python', 'python sex')''')
conn.commit()
conn.close()