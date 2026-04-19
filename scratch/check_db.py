
import sqlite3
import os

DB_PATH = os.path.join('data', 'companion.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('SELECT * FROM mood_logs')
rows = cursor.fetchall()
print(f"Total mood logs: {len(rows)}")
for row in rows[-5:]:
    print(row)
conn.close()
