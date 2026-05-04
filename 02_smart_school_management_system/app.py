from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def db():
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    return conn

def init():
    conn = db()
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        guardian_email TEXT,
        enrollment_date TEXT
    );
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        score REAL
    );
    ''')
    if conn.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 0:
        conn.executemany("INSERT INTO students(first_name,last_name,guardian_email,enrollment_date) VALUES(?,?,?,?)", [
            ("Amina","Khan","amina.guardian@example.com","2025-01-10"),
            ("Daniel","Mensah","daniel.guardian@example.com","2025-01-10"),
            ("Sofia","Lopez","sofia.guardian@example.com","2025-01-11")
        ])
        conn.executemany("INSERT INTO grades(student_id,subject,score) VALUES(?,?,?)", [
            (1,"Computer Studies",88),(2,"Computer Studies",76),(3,"Computer Studies",91)
        ])
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = db()
    students = conn.execute("SELECT * FROM students").fetchall()
    avg = conn.execute("SELECT ROUND(AVG(score),1) FROM grades").fetchone()[0]
    conn.close()
    return render_template("index.html", students=students, avg=avg)

@app.route("/add", methods=["POST"])
def add():
    conn = db()
    conn.execute("INSERT INTO students(first_name,last_name,guardian_email,enrollment_date) VALUES(?,?,?,?)",
                 (request.form["first_name"], request.form["last_name"], request.form["guardian_email"], request.form["enrollment_date"]))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init()
    app.run(debug=True)
