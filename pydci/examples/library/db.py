
import sqlite3

conn = sqlite3.connect('library.db')

cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, name)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS membership (
        id PRIMARY KEY, 
        member_id REFERENCES members (id) ON DELETE CASCADE, 
        password )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title, author, accession_id)''')
conn.commit()



cursor.execute('select * from members join membership on members.id = membership.member_id')
print(cursor.fetchall())

conn.close()


# cursor.execute('''INSERT INTO books (title, author, accession_id) VALUES ('moby dick', 'vladi', '2018p')''')




