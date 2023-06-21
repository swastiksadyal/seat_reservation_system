from flask import Flask, render_template, request, redirect
import sqlite3

conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

app = Flask(__name__)

e_mail = ""


@app.route('/')
def index():
    # Fetch all entries from the database
    c.execute("SELECT * FROM users")
    entries = c.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/add_user', methods=['POST'])
def add_user():
     # Retrieve data from the form
    name = request.form['name']
    email = request.form['email']
    
    c.execute("SELECT name FROM users WHERE email = ?", (email,))
    name = c.fetchone()
    if name: return book_seats(mail=email)
    # Insert new entry into the database
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email,))
    conn.commit()

    return book_seats(mail=email)

@app.route('/error')
def error():
    e = "Not enougḣ seats"
    seats = []
    c.execute("SELECT * FROM seats")
    seats_table = c.fetchall()
    for row in seats_table:
        seats.append(list(row[1:]))
    return render_template("error.html",data = {"seats": seats, "error":e, "email":e_mail})

@app.route('/book')
def book_seats(seats_booked:list=[], new_seats:list = [], e:str = "", mail:str="Not found"):
    seats =[]
    global e_mail
    e_mail = mail
    if (len(new_seats) < 1):
        c.execute("SELECT * FROM seats")
        seats_table = c.fetchall()
        for row in seats_table:
            seats.append(list(row[1:]))
    else:
        seats, seats_booked_db_entry = create_seats_table(seats_booked=seats_booked, seats=new_seats)
        update_data(seats_booked_db_entry, e_mail, seats)
    c.execute("SELECT seats_booked FROM users WHERE email = ?", (e_mail,))
    seats_booked_for_mail = c.fetchone()[0]
    if seats_booked_for_mail:
        seats_booked_for_mail = make_tuples(seats_booked_for_mail)
        seats, seats_booked_db_entry = create_seats_table(seats_booked=seats_booked_for_mail, seats=seats)
    if getLimit(0):
        return redirect("/error", code=302)
    return render_template("bookSeats.html",data = {"seats": seats, "error":e, "email":e_mail})

@app.route('/book_seats', methods=['POST'])
def book_seats_form():
    num_seats = int(request.form['seats_required'])
    c.execute("SELECT * FROM seats")
    seats_table = c.fetchall()
    seats = []
    for row in seats_table:
        seats.append(list(row[1:]))
    if getLimit(num_seats):
        return redirect("/error", code=302)
    seats_booked, new_seats = book(num_seats, seats) # type: ignore
    if getLimit(0):
        return redirect("/error", code=302)
    return book_seats(seats_booked=seats_booked, new_seats=new_seats, mail=e_mail)

def book(n:int, seats:list):
    booked = []
    try:
        for i in range(len(seats)):
            if n <= 0: return booked, seats
            seats_available = 7 - sum(seats[i])
            if n <= seats_available:
                for j in range(len(seats[i])):
                    if seats[i][j] == 0:
                        booked.append((i, j))
                        c.execute("UPDATE seats SET c{0} = ? WHERE row = ?".format(j+1), (1, i+1))
                        conn.commit()
                        seats[i][j] = 2
                        n -= 1
                        if n <= 0:
                            return booked, seats
        return booked, seats
    except IndexError:
        return redirect("/error", code=302)
        
def create_seats_table(seats_booked, seats):
    seats_booked_db = []
    new_seats =seats
    for i in range(len(seats_booked)):
        s = f"r{seats_booked[i][0]}-c{seats_booked[i][1]}"
        seats_booked_db.append(s)
        new_seats[seats_booked[i][0]][seats_booked[i][1]] = 2
    return new_seats, ','.join(seats_booked_db)

def make_tuples(li):
    res = []
    li = li.split(",")
    if li[0]=="0": 
        return []
    def f(s:str):
        r,c = int(s.split("-")[0][1:]), int(s.split("-")[1][1:])
        return r,c
    for s in li:
        R, C = f(s)
        res.append((R,C),)
    return res

def update_data(data:str, mail:str, seats:list):
    try:
        if data[0] == "0": return ""
    except IndexError:
        return error()
    c.execute("SELECT seats_booked FROM users WHERE email = ?", (mail,))
    seats_booked = c.fetchone()[0]
    if seats_booked:
        current_seats_booked = seats_booked
        new_seats_booked = current_seats_booked + ',' + data
    else:
        new_seats_booked = data
    c.execute("UPDATE users SET seats_booked = ? WHERE email = ?", (new_seats_booked, mail))
    conn.commit()
    return

def getLimit(n:int):
    seats = []
    c.execute("SELECT * FROM seats")
    seats_table = c.fetchall()
    for row in seats_table:
        seats.append(list(row[1:]))
    sm = n
    for i in range(len(seats)):
        for j in range(len(seats[i])):
            if seats[i][j] == 2:
                sm += 1
            elif seats[i][j] == -1:
                sm += 0
            else:
                sm += seats[i][j]
    if sm > 80:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
