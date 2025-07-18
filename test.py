import sqlite3

with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(students)')
    print(cursor.fetchall())

    cursor.execute('PRAGMA table_info(marks)')
    print(cursor.fetchall())
