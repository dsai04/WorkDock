from flask import Flask, request, session, render_template
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure database file exists
def get_db():
    conn = sqlite3.connect('workdock.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, role TEXT, level TEXT, location TEXT,
            experience TEXT, allowances TEXT, type TEXT, qualification TEXT,
            skills TEXT, salary INTEGER, email TEXT, number TEXT, other TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, profession TEXT, location TEXT, experience TEXT,
            dob TEXT, type TEXT, qualification TEXT, skills TEXT,
            salary INTEGER, email TEXT, number TEXT
        )''')

init_db()

# ------------------------------
# Authentication routes
# ------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with get_db() as db:
            try:
                db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
                return "Signup successful"
            except sqlite3.IntegrityError:
                return "Email already exists"
    return render_template('SIGNUP.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        if user:
            session['user'] = email
            return "Signed in successfully"
        else:
            return "Invalid credentials"
    return render_template('signin.html')


# ------------------------------
# Form submissions
# ------------------------------

@app.route('/submit_company', methods=['POST'])
def submit_company():
    data = {
        "name": request.form['name'],
        "role": request.form['role'],
        "level": request.form['level'],
        "location": request.form['location'],
        "experience": request.form['experience'],
        "allowances": request.form['allowences'],
        "type": request.form['type'],
        "qualification": request.form['qualification'],
        "skills": request.form['skills'],
        "salary": request.form['salaray'],
        "email": request.form['email'],
        "number": request.form['number'],
        "other": request.form['other']
    }
    with get_db() as db:
        db.execute('''INSERT INTO companies (name, role, level, location, experience, allowances,
                      type, qualification, skills, salary, email, number, other)
                      VALUES (:name, :role, :level, :location, :experience, :allowances,
                      :type, :qualification, :skills, :salary, :email, :number, :other)''', data)
    return "Company data submitted successfully."


@app.route('/submit_user', methods=['POST'])
def submit_user():
    data = {
        "name": request.form['txtname'],
        "profession": request.form['profession'],
        "location": request.form['location'],
        "experience": request.form['experience'],
        "dob": request.form['dob'],
        "type": request.form['time'],
        "qualification": request.form['qualification'],
        "skills": request.form['skills'],
        "salary": request.form['salary'],
        "email": request.form['email'],
        "number": request.form['number']
    }
    with get_db() as db:
        db.execute('''INSERT INTO user_data (name, profession, location, experience, dob, type,
                      qualification, skills, salary, email, number)
                      VALUES (:name, :profession, :location, :experience, :dob, :type,
                      :qualification, :skills, :salary, :email, :number)''', data)
    return "User data submitted successfully."


# ------------------------------
# Pages for rendering templates
# ------------------------------

@app.route('/')
def home():
    return render_template('signin.html')

@app.route('/company')
def company_page():
    return render_template('company.html')

@app.route('/user')
def user_page():
    return render_template('user.html')

# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)
