from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import subprocess
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from security.auth import verify
import random

app = Flask(__name__)
CORS(app)

# Global state to hold live camera data
current_analytics = {
    "students_present": 0,
    "engagement_score": 0
}

@app.route("/")
def home():
    return "AI Classroom Analytics Backend Running"


@app.route("/start_camera", methods=["POST"])
def start_camera():
    key = request.headers.get("x-api-key")
    if not verify(key):
        return jsonify({"error": "Unauthorized access"}), 401
    
    try:
        subprocess.Popen([sys.executable, "model/classroom_analytics.py"])
        return jsonify({"status": "Camera started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_analytics", methods=["POST"])
def update_analytics():
    key = request.headers.get("x-api-key")
    if not verify(key):
        return jsonify({"error": "Unauthorized access"}), 401
    
    data = request.json
    if data:
        current_analytics["students_present"] = data.get("students_present", 0)
        current_analytics["engagement_score"] = data.get("engagement_score", 0)
    
    return jsonify({"status": "success"})


@app.route("/analytics")
def analytics():

    # ---- Security check ----
    key = request.headers.get("x-api-key")

    if not verify(key):
        return jsonify({"error": "Unauthorized access"}), 401

    # Return live data from camera instead of random simulated data
    return jsonify(current_analytics)


@app.route("/health")
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)