from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

import os

BASE = os.path.dirname(os.path.abspath(__file__))

def conn():
    return sqlite3.connect(os.path.join(BASE, "database.db"))



@app.route("/")
def home():
    return "Technician Panel Backend Running ✔"


# GET jobs for a team
@app.route("/tech/jobs")
def tech_jobs():
    with conn() as c:
        rows = c.execute("""
            SELECT id, equipment, description, status, team
            FROM requests
        """).fetchall()

    return jsonify([
        {
            "id": r[0],
            "equipment": r[1],
            "description": r[2],
            "status": r[3],
            "team": r[4]
        }
        for r in rows
    ])


# Update status
@app.route("/tech/status/<int:id>", methods=["PUT"])
def tech_update(id):
    status = request.json["status"]

    with conn() as c:
        c.execute("UPDATE requests SET status=? WHERE id=?", (status, id))
        c.commit()

    return jsonify({"message": "Updated"})

@app.route("/tech/claim/<int:id>", methods=["PUT"])
def claim_job(id):
    data = request.json
    with conn() as c:
        c.execute("""
            UPDATE requests
            SET status=?, assigned_to=?
            WHERE id=?
        """, (data["status"], data["tech"], id))
        c.commit()

    return jsonify({"message": "Updated"})
@app.route("/tech/update/<int:id>", methods=["PUT"])
def tech_update_job(id):
    data = request.json
    with conn() as c:
        c.execute("""
            UPDATE requests
            SET status=?, tech_note=?
            WHERE id=?
        """, (data["status"], data["note"], id))
        c.commit()

    return jsonify({"message": "Updated"})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
