import os
from flask import Flask, jsonify

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "unknown")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
GREETING = os.getenv("GREETING", "Hello from Helm!")


@app.route("/")
def home():
    return jsonify(
        message=GREETING,
        environment=APP_ENV,
        version=APP_VERSION,
        pod=os.getenv("HOSTNAME", "local"),
    )


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
