from flask import Flask, jsonify, request
from ..security.auth import verify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Classroom Analytics Backend Running"


@app.route("/analytics")
def analytics():

    # ---- Security check ----
    key = request.headers.get("x-api-key")

    if not verify(key):
        return jsonify({"error": "Unauthorized access"}), 401

    # ---- Simulated analytics result ----
    students = random.randint(3,10)
    engagement = min(students * 10, 100)

    data = {
        "students_present": students,
        "engagement_score": engagement
    }

    return jsonify(data)


@app.route("/health")
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)