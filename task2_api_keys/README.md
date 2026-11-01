# Task 2: API Key Generation and Sharing

The API exposes `POST /process` and requires an `X-API-Key` header. Keys are generated with Python's `secrets` module at startup and are printed only to the server console. They are intentionally not committed to the repository.

## Run

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Copy the three generated keys from the terminal to the assigned testers through a private channel. Do not publish them in the repository, screenshots, or video.

## cURL tests

```bash
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: <CONSUMER_1_KEY>" -d "{\"text\":\"hello rootsoftware\"}"
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: <CONSUMER_2_KEY>" -d "{\"text\":\"another test\"}"
curl -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: <CONSUMER_3_KEY>" -d "{\"text\":\"third test\"}"
curl -i -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -H "X-API-Key: invalid-key" -d "{\"text\":\"should fail\"}"
curl -i -X POST http://127.0.0.1:5002/process -H "Content-Type: application/json" -d "{\"text\":\"should fail\"}"
```

Valid requests return uppercase text. Invalid or missing keys return HTTP 401.

## Video

See `DEMO_VIDEO_LINK.txt`. Keep the keys masked in the recording.

