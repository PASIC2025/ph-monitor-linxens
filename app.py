from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__)  # uses 'templates' and 'static' by default
CORS(app)

# In-memory storage of pH data (lost when server restarts)
PH_DATA_STORE = []


# --- 1. Frontend route ---
@app.route("/")
def index():
    # Renders templates/index.html
    return render_template("index.html")


# --- 2. Health check for Render ---
@app.route("/healthz")
def healthz():
    return "ok", 200


# --- 3. Endpoint for device to POST pH data ---
@app.route("/api/ph-data", methods=["POST"])
def post_ph_data():
    data = request.get_json(force=True) or {}

    ph = data.get("ph")
    timestamp = data.get("timestamp")

    # Basic validation
    if ph is None:
        return jsonify({"error": "Missing 'ph' field"}), 400

    # If no timestamp provided, use current UTC time
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat() + "Z"

    entry = {
        "ph": ph,
        "timestamp": timestamp,
    }
    PH_DATA_STORE.append(entry)

    # Optional: keep only the last N entries
    if len(PH_DATA_STORE) > 1000:
        PH_DATA_STORE.pop(0)

    return jsonify({"status": "ok"}), 201


# --- 4. Endpoint for webpage to GET pH data ---
@app.route("/api/ph-data", methods=["GET"])
def get_ph_data():
    return jsonify(PH_DATA_STORE)

# --- 5. Endpoint to clear all stored pH data ---
@app.route("/api/ph-data", methods=["DELETE"])
def clear_ph_data():
    PH_DATA_STORE.clear()
    return jsonify({"status": "cleared"}), 200


if __name__ == "__main__":
    # Local dev: default to 5000; Render uses PORT env var (via gunicorn)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
