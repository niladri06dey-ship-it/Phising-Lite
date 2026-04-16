# ============================================================
# PhishNet Lite - FINAL Backend
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import re, requests, os, datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- MONGODB ----------------
client = MongoClient(os.getenv("MONGO_URI"))
db = client["phishnet"]
collection = db["logs"]

# ---------------- HOME ROUTE (IMPORTANT) ----------------
@app.route('/')
def home():
    return "🛡️ PhishNet Lite Backend is Running"

# ---------------- RULE-BASED ----------------
def rule_based_detection(url):
    score = 0
    url_lower = url.lower()

    if url.startswith("http://"):
        score += 2

    if any(k in url_lower for k in [
        "login","verify","secure","password",
        "update","account","bank","signin"
    ]):
        score += 2

    if len(url) > 60:
        score += 1

    if "@" in url:
        score += 3

    if any(d in url_lower for d in [".xyz",".tk",".ml",".ga"]):
        score += 2

    if url.count('.') > 3:
        score += 2

    if re.search(r'\d{1,3}(\.\d{1,3}){3}', url):
        score += 3

    return score

# ---------------- VALIDATION ----------------
def is_valid_url(url):
    return bool(re.match(r'^(https?://)?([a-z0-9.-]+)\.([a-z]{2,})', url, re.I))

# ---------------- MAIN API ----------------
@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    url = data.get('url', '')

    if not url or not is_valid_url(url):
        result = {
            "result": "Phishing ❌",
            "label": "Phishing",
            "class": "phishing",
            "source": "Invalid URL"
        }
    else:
        score = rule_based_detection(url)

        if score >= 5:
            result = {
                "result": "Phishing ❌",
                "label": "Phishing",
                "class": "phishing",
                "source": "Rule Engine"
            }
        else:
            result = {
                "result": "Safe ✅",
                "label": "Safe",
                "class": "safe",
                "source": "No threat detected"
            }

    # Save to MongoDB
    try:
        collection.insert_one({
            "url": url,
            **result,
            "time": datetime.datetime.utcnow()
        })
    except:
        pass

    return jsonify(result)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))