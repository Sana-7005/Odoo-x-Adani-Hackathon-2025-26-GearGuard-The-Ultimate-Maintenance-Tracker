from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB = "database.db"

def conn():
    return sqlite3.connect(DB)

# -------- INITIALIZE DATABASE --------
with conn() as c:
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            role TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS requests(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            equipment TEXT,
            team TEXT,
            description TEXT,
            status TEXT DEFAULT 'New',
            tech_note TEXT DEFAULT '',
            assigned_to TEXT DEFAULT ''
        )
    """)

    c.commit()


# -------- LOGIN (Mock user exists automatically) --------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]

    with conn() as c:
        user = c.execute("SELECT name,email,role FROM users WHERE email=?",
                         (email,)).fetchone()

        if not user:
            c.execute("INSERT INTO users(name,email,role) VALUES(?,?,?)",
                      (data["name"], email, "employee"))
            c.commit()
            user = (data["name"], email, "employee")

    return jsonify({"user": {"name": user[0], "email": user[1], "role": user[2]}})


# -------- CREATE REQUEST --------
@app.route("/requests", methods=["POST"])
def create_request():
    data = request.json

    with conn() as c:
        c.execute("""
            INSERT INTO requests(user_email,equipment,team,description)
            VALUES(?,?,?,?)
        """, (
            data["email"],
            data["equipment"],
            data["team"],
            data["description"]
        ))
        c.commit()

    return jsonify({"message": "Request saved!"})


# -------- GET REQUESTS FOR A USER --------
@app.route("/requests/<email>")
def get_requests(email):
    with conn() as c:
        rows = c.execute("""
            SELECT id,equipment,team,description,status
            FROM requests
            WHERE user_email=?
        """, (email,)).fetchall()

    return jsonify([
        {
            "id": r[0],
            "equipment": r[1],
            "team": r[2],
            "description": r[3],
            "status": r[4],
        }
        for r in rows
    ])
@app.route("/requests/status/<int:id>", methods=["PUT"])
def update_status(id):
    status = request.json["status"]

    with conn() as c:
        c.execute("UPDATE requests SET status=? WHERE id=?", (status, id))
        c.commit()

    return jsonify({"message": "Status updated!"})


if __name__ == "__main__":
    app.run(debug=True)
