# ============================================================
# PhishNet Lite - FINAL Backend (Production Ready)
# ============================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------------- MONGODB ----------------
client = MongoClient(os.getenv("MONGO_URI"))
db = client["phishnet"]
collection = db["logs"]

# ---------------- RULE-BASED ----------------
def rule_based_detection(url):
    score = 0
    url_lower = url.lower()

    if url.startswith("http://"):
        score += 2

    keywords = [
        "login", "verify", "secure", "password",
        "update", "account", "bank", "signin"
    ]
    if any(word in url_lower for word in keywords):
        score += 2

    if len(url) > 60:
        score += 1

    if "@" in url:
        score += 3

    if any(domain in url_lower for domain in [".xyz", ".tk", ".ml", ".ga"]):
        score += 2

    if url.count('.') > 3:
        score += 2

    if re.search(r'\d{1,3}(\.\d{1,3}){3}', url):
        score += 3

    return score


# ---------------- GOOGLE SAFE ----------------
def check_google(url):
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        return False

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    payload = {
        "client": {"clientId": "phishnet-lite", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        res = requests.post(endpoint, json=payload, timeout=5)
        return res.status_code == 200 and "matches" in res.json()
    except:
        return False


# ---------------- VIRUSTOTAL ----------------
def check_virustotal(url):
    API_KEY = os.getenv("VT_API_KEY")
    if not API_KEY:
        return False

    headers = {"x-apikey": API_KEY}

    try:
        res = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if res.status_code != 200:
            return False

        analysis_id = res.json()["data"]["id"]

        report = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        stats = report.json()["data"]["attributes"]["stats"]
        malicious = stats.get("malicious", 0)

        return malicious >= 2

    except:
        return False


# ---------------- VALIDATION ----------------
def is_valid_url(url):
    pattern = re.compile(
        r'^(https?://)?([a-z0-9.-]+)\.([a-z]{2,})',
        re.IGNORECASE
    )
    return bool(pattern.match(url))


# ---------------- MAIN API ----------------
@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    url = data.get('url', '')

    if not url or not is_valid_url(url):
        result_data = {
            "result": "Phishing ❌",
            "label": "Phishing",
            "class": "phishing",
            "source": "Invalid URL"
        }

    else:
        score = rule_based_detection(url)
        google_flag = check_google(url)
        vt_flag = check_virustotal(url)

        sources = []

        if google_flag:
            sources.append("Google Safe Browsing")

        if vt_flag:
            sources.append("VirusTotal")

        if score >= 5:
            sources.append("Rule Engine")

        if sources:
            result_data = {
                "result": "Phishing ❌",
                "label": "Phishing",
                "class": "phishing",
                "source": ", ".join(sources)
            }
        else:
            result_data = {
                "result": "Safe ✅",
                "label": "Safe",
                "class": "safe",
                "source": "No threat detected"
            }

    # ---------------- SAVE TO MONGODB ----------------
    try:
        collection.insert_one({
            "url": url,
            **result_data,
            "time": datetime.datetime.utcnow()
        })
    except Exception as e:
        print("MongoDB Error:", e)

    return jsonify(result_data)


# ---------------- HISTORY (OPTIONAL) ----------------
@app.route('/history', methods=['GET'])
def history():
    data = list(collection.find({}, {"_id": 0}).sort("time", -1).limit(10))
    return jsonify(data)


# ---------------- RUN ----------------
if __name__ == "__main__":
    print("🛡️ PhishNet running...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))