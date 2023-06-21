import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              Name TEXT,
              email TEXT,
              seats_booked TEXT)''')
conn.commit()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS seats
             (row INTEGER,
              c1 INTEGER,
              c2 INTEGER,
              c3 INTEGER,c4 INTEGER,c5 INTEGER,c6 INTEGER,c7 INTEGER)''')
conn.commit()

for i in range(11):
    c.execute("INSERT INTO seats (row, c1, c2, c3, c4, c5, c6, c7) VALUES (?,?,?,?,?,?,?,?)", (i+1,0,0,0,0,0,0,0))
    conn.commit()
c.execute("INSERT INTO seats (row, c1, c2, c3, c4, c5, c6, c7) VALUES (?,?,?,?,?,?,?,?)", (12,0,0,0,-1,-1,-1,-1))
conn.commit()

# c.execute("UPDATE seats SET c{0} = ? WHERE row = ?".format(3), (1, 2))
# conn.commit()

# c.execute("SELECT * FROM seats")
# seats_table = c.fetchall()
# seats = []
# for row in seats_table:
#     seats.append(list(row[1:]))
# def create_seats_table(seats_booked, seats):
#     seats_booked_db = []
#     new_seats =seats
#     for i in range(len(seats_booked)):
#         s = "r{seats_booked[i][0]}-c{seats_booked[i][1]}"
#         seats_booked_db.append(s)
#         new_seats[seats_booked[i][0]][seats_booked[i][1]] = 2
#     return new_seats, ','.join(seats_booked_db)

# def make_tuples(li):
#     res = []
#     li = li.split(",")
#     if li[0]=="0": 
#         return []
#     def f(s:str):
#         r,c = int(s.split("-")[0][1:]), int(s.split("-")[1][1:])
#         return r,c
#     for s in li:
#         R, C = f(s)
#         res.append((R,C))
#     return res

mail = "asda@mail.com"
# def update_data(data:str, mail:str):
#     if data[0] == "0": return ""
#     c.execute("SELECT seats_booked FROM users WHERE email = ?", (mail,))
#     seats_booked = c.fetchone()
#     if seats_booked:
#         current_seats_booked = seats_booked[0]
#         new_seats_booked = current_seats_booked + ', ' + data
#     else:
#         new_seats_booked = data
#     c.execute("UPDATE users SET seats_booked = ? WHERE email = ?", (new_seats_booked, mail))
#     conn.commit()
#     return new_seats_booked


# c.execute("SELECT seats_booked FROM users WHERE email = ?", (mail,))
# s = c.fetchone()
# def make_tuples(li):
#     res = []
#     li = li.split(",")
#     if li[0]=="0": 
#         return []
#     def f(s:str):
#         r,c = int(s.split("-")[0][1:]), int(s.split("-")[1][1:])
#         return r,c
#     for s in li:
#         R, C = f(s)
#         res.append((R,C))
#     return res

# def getLimit():
#     seats = []
#     c.execute("SELECT * FROM seats")
#     seats_table = c.fetchall()
#     for row in seats_table:
#         seats.append(list(row[1:]))
#     sm = 0
#     for i in range(len(seats)):
#         for j in range(len(seats[i])):
#             if seats[i][j] == 2:
#                 sm += 1
#             elif seats[i][j] == -1:
#                 sm += 0
#             else:
#                 sm += seats[i][j]
#     print(sm)
#     if sm > 80:
#         return True
#     return False
# print(getLimit())
# print(s)
# print(s[0])
# print(make_tuples(s[0]))
conn.close()
