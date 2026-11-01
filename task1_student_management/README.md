# Task 1: Database-Driven Flask API with Streamlit

This task uses SQLite for persistence, Flask for the REST API, and Streamlit for the user interface.

## Run

From this folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

In another terminal, run:

```bash
streamlit run streamlit_app.py
```

The API runs at `http://127.0.0.1:5001` and Streamlit normally opens at `http://localhost:8501`.

The SQLite database is created automatically as `students.db`. The Streamlit page refreshes after add, update, and delete operations.

## cURL examples

```bash
curl http://127.0.0.1:5001/students
curl http://127.0.0.1:5001/students/1
curl -X POST http://127.0.0.1:5001/students -H "Content-Type: application/json" -d "{\"name\":\"Ayesha Khan\",\"department\":\"Computer Science\",\"email\":\"ayesha@example.com\"}"
curl -X PUT http://127.0.0.1:5001/students/1 -H "Content-Type: application/json" -d "{\"name\":\"Ayesha Khan Updated\",\"department\":\"Software Engineering\",\"email\":\"ayesha.updated@example.com\"}"
curl -X DELETE http://127.0.0.1:5001/students/1
```

## Video

See `DEMO_VIDEO_LINK.txt`. Replace its placeholder with a public video link before submission.

