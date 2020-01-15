import sqlite3

conn = sqlite3.connect('old_users.db')
c = conn.cursor()
c.execute("SELECT * FROM users"
          , )
users = c.fetchall()
conn.commit()
NONE_place = 'NaP'
conn = sqlite3.connect('users.db')
c = conn.cursor()
for user in users:
    account_name, account_id, hostel = user[:3]
    command, time = user[4:]
    prev = user[3]
    if prev != NONE_place:
        prev = user[3].replace('(', ' ').replace(')', ' ')
        new = prev.split()
        if len(new):
            new.append(NONE_place)
        c.execute("""
                INSERT INTO users VALUES (?,?,?,?,?,?,?) 
            """, (account_name, account_id, hostel, new[0], new[1], command, time))
    else:
        c.execute("""
                INSERT INTO users VALUES (?,?,?,?,?,?,?) 
            """, (account_name, account_id, hostel, NONE_place, NONE_place, command, time))

users = c.fetchall()
conn.commit()
