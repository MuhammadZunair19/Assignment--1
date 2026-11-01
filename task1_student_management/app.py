from pathlib import Path
import sqlite3
from flask import Flask, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"
app = Flask(__name__)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )""")
        db.commit()


def student_dict(row):
    return dict(row)


@app.get("/students")
def list_students():
    with get_db() as db:
        rows = db.execute("SELECT id, name, department, email FROM students ORDER BY id").fetchall()
    return jsonify([student_dict(row) for row in rows])


@app.get("/students/<int:student_id>")
def get_student(student_id):
    with get_db() as db:
        row = db.execute("SELECT id, name, department, email FROM students WHERE id = ?", (student_id,)).fetchone()
    if row is None:
        return jsonify(error="Student not found"), 404
    return jsonify(student_dict(row))


def validate_student_payload(payload):
    if not isinstance(payload, dict):
        return "JSON object is required"
    required = ("name", "department", "email")
    missing = [field for field in required if not str(payload.get(field, "")).strip()]
    return f"Missing required fields: {', '.join(missing)}" if missing else None


@app.post("/students")
def create_student():
    payload = request.get_json(silent=True)
    error = validate_student_payload(payload)
    if error:
        return jsonify(error=error), 400
    try:
        with get_db() as db:
            cursor = db.execute("INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
                                (payload["name"].strip(), payload["department"].strip(), payload["email"].strip()))
            db.commit()
            row = db.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return jsonify(student_dict(row)), 201
    except sqlite3.IntegrityError:
        return jsonify(error="Email must be unique"), 409


@app.put("/students/<int:student_id>")
def update_student(student_id):
    payload = request.get_json(silent=True)
    error = validate_student_payload(payload)
    if error:
        return jsonify(error=error), 400
    try:
        with get_db() as db:
            cursor = db.execute("UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?",
                                (payload["name"].strip(), payload["department"].strip(), payload["email"].strip(), student_id))
            if cursor.rowcount == 0:
                return jsonify(error="Student not found"), 404
            db.commit()
            row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        return jsonify(student_dict(row))
    except sqlite3.IntegrityError:
        return jsonify(error="Email must be unique"), 409


@app.delete("/students/<int:student_id>")
def delete_student(student_id):
    with get_db() as db:
        cursor = db.execute("DELETE FROM students WHERE id = ?", (student_id,))
        db.commit()
    if cursor.rowcount == 0:
        return jsonify(error="Student not found"), 404
    return jsonify(message="Student deleted")


init_db()

if __name__ == "__main__":
    app.run(port=5001, debug=True)

