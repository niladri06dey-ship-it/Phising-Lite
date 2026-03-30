async function checkPhishing() {
    const url = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("result");

    if (!url) {
        resultDiv.innerText = "⚠️ Please enter a URL";
        resultDiv.className = "result warning";
        return;
    }

    resultDiv.innerText = "Checking... ⏳";

    try {
        const response = await fetch("http://127.0.0.1:5000/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        resultDiv.innerText = data.result;
        resultDiv.className = "result " + data.class;

    } catch (error) {
        resultDiv.innerText = "❌ Server not running";
        resultDiv.className = "result danger";
    }
}