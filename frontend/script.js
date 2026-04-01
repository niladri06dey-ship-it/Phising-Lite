// --------- PHISHING CHECK ----------
async function checkPhishing() {
    const url = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("result");
    const progressBar = document.getElementById("progressBar");

    if (!url) {
        resultDiv.innerText = "⚠️ Enter a URL";
        return;
    }

    resultDiv.innerText = "Scanning... ⚡";
    progressBar.style.width = "20%";

    try {
        const res = await fetch("http://127.0.0.1:5000/check", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({url})
        });

        const data = await res.json();

        resultDiv.innerText = data.result;

        let percent = data.class === "safe" ? 90 :
                      data.class === "warning" ? 50 : 20;

        progressBar.style.width = percent + "%";

    } catch {
        resultDiv.innerText = "❌ Server not running";
        progressBar.style.width = "0%";
    }
}

// --------- PARTICLES ----------
const canvas = document.getElementById("bgCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];

for (let i = 0; i < 80; i++) {
    particles.push({
        x: Math.random()*canvas.width,
        y: Math.random()*canvas.height,
        r: Math.random()*2,
        dx: Math.random()-0.5,
        dy: Math.random()-0.5
    });
}

function animate() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    particles.forEach(p=>{
        ctx.beginPath();
        ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
        ctx.fillStyle="#38bdf8";
        ctx.fill();

        p.x+=p.dx;
        p.y+=p.dy;

        if(p.x<0||p.x>canvas.width) p.dx*=-1;
        if(p.y<0||p.y>canvas.height) p.dy*=-1;
    });

    requestAnimationFrame(animate);
}

animate();

window.addEventListener("resize",()=>{
    canvas.width=window.innerWidth;
    canvas.height=window.innerHeight;
});