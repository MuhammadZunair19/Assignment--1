import base64
import hashlib
import hmac
import json
import os
import time
from functools import wraps
from flask import Flask, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
TOKEN_SECRET = os.getenv("TOKEN_SECRET", "classroom-demo-secret-change-me").encode()
USERS = {
    "employee": {"password": generate_password_hash("employee123"), "role": "employee"},
    "admin": {"password": generate_password_hash("admin123"), "role": "administrator"},
}
EMPLOYEES = {
    1: {"id": 1, "name": "Sara Ahmed", "department": "Human Resources"},
    2: {"id": 2, "name": "Bilal Khan", "department": "Engineering"},
}


def encode_token(username, role):
    payload = json.dumps({"sub": username, "role": role, "exp": int(time.time()) + 3600}, separators=(",", ":")).encode()
    body = base64.urlsafe_b64encode(payload).rstrip(b"=")
    signature = hmac.new(TOKEN_SECRET, body, hashlib.sha256).digest()
    return body.decode() + "." + base64.urlsafe_b64encode(signature).rstrip(b"=").decode()


def decode_token(token):
    try:
        body_text, signature_text = token.split(".", 1)
        body = body_text.encode()
        expected = hmac.new(TOKEN_SECRET, body, hashlib.sha256).digest()
        supplied = base64.urlsafe_b64decode(signature_text + "=" * (-len(signature_text) % 4))
        if not hmac.compare_digest(expected, supplied):
            return None
        payload = json.loads(base64.urlsafe_b64decode(body + b"=" * (-len(body) % 4)))
        return payload if payload["exp"] >= time.time() else None
    except (ValueError, KeyError, json.JSONDecodeError, base64.binascii.Error):
        return None


def auth_required(admin_only=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            token = header[7:] if header.startswith("Bearer ") else ""
            user = decode_token(token)
            if user is None:
                return jsonify(error="Authentication required"), 401
            if admin_only and user["role"] != "administrator":
                return jsonify(error="Administrator role required"), 403
            return function(*args, **kwargs)
        return wrapper
    return decorator


@app.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    user = USERS.get(payload.get("username"))
    if user is None or not check_password_hash(user["password"], payload.get("password", "")):
        return jsonify(error="Invalid username or password"), 401
    return jsonify(access_token=encode_token(payload["username"], user["role"]), role=user["role"])


@app.get("/employees")
@auth_required()
def list_employees():
    return jsonify(list(EMPLOYEES.values()))


@app.post("/employees")
@auth_required(admin_only=True)
def add_employee():
    payload = request.get_json(silent=True) or {}
    if not payload.get("name") or not payload.get("department"):
        return jsonify(error="name and department are required"), 400
    new_id = max(EMPLOYEES, default=0) + 1
    EMPLOYEES[new_id] = {"id": new_id, "name": payload["name"], "department": payload["department"]}
    return jsonify(EMPLOYEES[new_id]), 201


@app.put("/employees/<int:employee_id>")
@auth_required(admin_only=True)
def update_employee(employee_id):
    if employee_id not in EMPLOYEES:
        return jsonify(error="Employee not found"), 404
    payload = request.get_json(silent=True) or {}
    if not payload.get("name") or not payload.get("department"):
        return jsonify(error="name and department are required"), 400
    EMPLOYEES[employee_id].update(name=payload["name"], department=payload["department"])
    return jsonify(EMPLOYEES[employee_id])


@app.delete("/employees/<int:employee_id>")
@auth_required(admin_only=True)
def delete_employee(employee_id):
    if EMPLOYEES.pop(employee_id, None) is None:
        return jsonify(error="Employee not found"), 404
    return jsonify(message="Employee deleted")


if __name__ == "__main__":
    app.run(port=5003, debug=False)

