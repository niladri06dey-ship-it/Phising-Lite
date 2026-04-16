# 🛡️ PhishNet Lite

Real-Time Phishing Detection Web Application

---

## 🚀 Overview

PhishNet Lite is a full-stack cybersecurity web application that detects phishing websites in real time.
It analyzes URLs using strict rule-based heuristics combined with threat intelligence APIs and stores results in a cloud database.

---

## ✨ Features

* 🔍 Real-time URL scanning
* 🧠 Rule-based phishing detection engine
* 🌐 Google Safe Browsing integration
* 🦠 VirusTotal API support
* 📊 MongoDB logging system
* ⚡ Fast and responsive UI
* 🎨 Futuristic animated interface

---

## 🧠 How It Works

1. User enters a URL
2. Frontend sends request to backend API
3. Backend analyzes URL using:

   * Rule-based detection
   * Google Safe Browsing
   * VirusTotal
4. Result is classified as:

   * ✅ Safe
   * ❌ Phishing
5. Data is stored in MongoDB for logging and analysis

---

## 🏗️ Tech Stack

**Frontend**

* HTML, CSS, JavaScript

**Backend**

* Python (Flask)
* Flask-CORS

**Database**

* MongoDB Atlas

**APIs**

* Google Safe Browsing API
* VirusTotal API

---

## 📁 Project Structure

```
PhishNet-Lite/
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/phishnet-lite.git
cd phishnet-lite
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file:

```
MONGO_URI=your_mongodb_connection_string
GOOGLE_API_KEY=your_google_api_key
VT_API_KEY=your_virustotal_api_key
```

---

### 4. Run Backend

```bash
cd backend
python app.py
```

---

### 5. Run Frontend

Open:

```
frontend/index.html
```

---

## 🌐 Deployment

**Backend:** Render
**Frontend:** Netlify

Update API URL in `script.js`:

```javascript
const API_URL = "https://your-backend.onrender.com/check";
```

---

## 📊 Future Improvements

* 🤖 Machine Learning model integration
* 📈 Analytics dashboard
* 🌍 Browser extension
* 🧾 Detailed phishing explanation system

---

## 👨‍💻 Team

* Niladri Dey
* Mayukh Pal
* Badhon Banerjee

---

## 💡 Inspiration

Built for hackathon innovation in cybersecurity to create a simple, fast, and effective phishing detection system.

---

## 📜 License

This project is for educational and research purposes.
