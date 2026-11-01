# Task 3: Authentication and Authorization

This API uses a signed bearer token. The demo users are created in memory at startup:

- Employee: username `employee`, password `employee123`
- Administrator: username `admin`, password `admin123`

These are classroom-only credentials; do not use them in production. Passwords are stored as Werkzeug hashes, not plaintext. Employee tokens can read records; administrator tokens can read, add, update, and delete records.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## cURL demonstration

Unauthenticated request — authentication failure (401):

```bash
curl -i http://127.0.0.1:5003/employees
```

Login as employee and save the returned token:

```bash
curl -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d "{\"username\":\"employee\",\"password\":\"employee123\"}"
```

Use the employee token to view records (200), then try an administrator-only operation (403):

```bash
curl http://127.0.0.1:5003/employees -H "Authorization: Bearer <EMPLOYEE_TOKEN>"
curl -i -X POST http://127.0.0.1:5003/employees -H "Authorization: Bearer <EMPLOYEE_TOKEN>" -H "Content-Type: application/json" -d "{\"name\":\"New Person\",\"department\":\"Finance\"}"
```

Login as administrator and use the returned token for all operations:

```bash
curl -X POST http://127.0.0.1:5003/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
curl -X POST http://127.0.0.1:5003/employees -H "Authorization: Bearer <ADMIN_TOKEN>" -H "Content-Type: application/json" -d "{\"name\":\"New Person\",\"department\":\"Finance\"}"
curl -X PUT http://127.0.0.1:5003/employees/1 -H "Authorization: Bearer <ADMIN_TOKEN>" -H "Content-Type: application/json" -d "{\"name\":\"Updated Person\",\"department\":\"Engineering\"}"
curl -X DELETE http://127.0.0.1:5003/employees/1 -H "Authorization: Bearer <ADMIN_TOKEN>"
```

Invalid credentials return 401. A valid employee token attempting an admin operation returns 403, demonstrating the difference between authentication and authorization.

## Video

See `DEMO_VIDEO_LINK.txt`. Mask tokens in the recording.

