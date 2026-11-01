import secrets
from flask import Flask, jsonify, request

app = Flask(__name__)
API_KEYS = {secrets.token_urlsafe(32): f"consumer_{number}" for number in range(1, 4)}


def print_keys_once():
    print("Generated testing keys (share privately; do not commit):")
    for key, consumer in API_KEYS.items():
        print(f"{consumer}: {key}")


@app.post("/process")
def process_text():
    supplied_key = request.headers.get("X-API-Key", "")
    consumer = API_KEYS.get(supplied_key)
    if consumer is None:
        return jsonify(error="Invalid or missing API key"), 401
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
        return jsonify(error="JSON field 'text' must be a string"), 400
    return jsonify(consumer=consumer, original=payload["text"], processed=payload["text"].upper())


if __name__ == "__main__":
    print_keys_once()
    app.run(port=5002, debug=False)

