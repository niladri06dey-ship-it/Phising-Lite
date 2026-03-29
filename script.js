// PhishNet Lite - Phishing Detection Logic

function checkPhishing() {
    const input = document.getElementById("urlInput");
    const resultDiv = document.getElementById("result");

    let url = input.value.trim().toLowerCase();

    // Empty input check
    if (url === "") {
        resultDiv.innerText = "⚠️ Please enter a URL";
        resultDiv.className = "result warning";
        return;
    }

    let score = 0;

    // Rule 1: '@' symbol (used in phishing)
    if (url.includes("@")) score += 2;

    // Rule 2: Long URL
    if (url.length > 75) score += 1;

    // Rule 3: Suspicious keywords
    const keywords = ["login", "verify", "bank", "secure", "account", "update"];
    for (let word of keywords) {
        if (url.includes(word)) {
            score += 2;
            break;
        }
    }

    // Rule 4: HTTP instead of HTTPS
    if (url.startsWith("http://")) score += 1;

    // Rule 5: IP address instead of domain
    const ipPattern = /\d{1,3}(\.\d{1,3}){3}/;
    if (ipPattern.test(url)) score += 2;

    // Final Classification
    let resultText = "";
    let resultClass = "";

    if (score >= 4) {
        resultText = "❌ Phishing Website Detected";
        resultClass = "danger";
    } else if (score >= 2) {
        resultText = "⚠️ Suspicious Website";
        resultClass = "warning";
    } else {
        resultText = "✅ Safe Website";
        resultClass = "safe";
    }

    // Show result
    resultDiv.innerText = resultText;
    resultDiv.className = "result " + resultClass;
}