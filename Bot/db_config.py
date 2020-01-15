import sqlite3
import sys

f = open('users.db', 'rb')
data = f.read()
f.close()
f = open('old_users.db', 'wb')
f.write(data)
f.close()
conn = sqlite3.connect("users.db")
DROP_value = True
c = conn.cursor()
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'drop':
        n = input("Drop database? y\\n")
        print('lol')
        if n.lower() == 'y':
            c.execute("""
                DROP TABLE IF EXISTS users                   
            """)
elif DROP_value:
    c.execute("""
                    DROP TABLE IF EXISTS users                   
                """)
c.execute("""CREATE TABLE IF NOT EXISTS users
              (account_name TEXT, account_id INTEGER  PRIMARY KEY, hostel TEXT, apartments TEXT, room TEXT, previous_command TEXT, last_change TEXT, vk TEXT ) 
           """)
conn = sqlite3.connect('old_users.db')
c = conn.cursor()
c.execute("SELECT * FROM users"
          , )
users = c.fetchall()
conn.commit()
NONE_vk = 'User haven\'t specified vk url'

NONE_place = 'NaP'
conn = sqlite3.connect('users.db')
c = conn.cursor()
for user in users:
    print(user)
    c.execute("""
            INSERT INTO users VALUES (?,?,?,?,?,?,?,?) 
        """, (user+(NONE_vk,)))

conn.commit()
