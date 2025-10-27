# main.py
import os
from flask import Flask, request, jsonify, Response
from openai import OpenAI

# Create Flask app
app = Flask(__name__)

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === HTML PAGE (embedded directly in this file) ===
HTML_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>ChatGPT Mini</title>
  <style>
    body { font-family: Arial, Helvetica, sans-serif; display:flex; align-items:center; justify-content:center; height:100vh; margin:0; background:#f5f7fa; }
    .card { width: 92%; max-width:720px; background:white; padding:20px; border-radius:10px; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
    #response { margin-top:16px; white-space:pre-wrap; }
    #message { width: calc(100% - 90px); padding:10px; border:1px solid #ddd; border-radius:6px; }
    button { padding:10px 14px; margin-left:8px; border-radius:6px; border:none; background:#2563eb; color:white; cursor:pointer; }
    button:disabled { background:#9bb7ff; cursor:default; }
    form { display:flex; align-items:center; }
  </style>
</head>
<body>
  <div class="card">
    <h2>ChatGPT Mini</h2>
    <form id="chatForm">
      <input id="message" placeholder="Type your message..." autocomplete="off" />
      <button type="submit">Send</button>
    </form>
    <div id="response"></div>
  </div>

  <script>
    const form = document.getElementById("chatForm");
    const messageInput = document.getElementById("message");
    const respDiv = document.getElementById("response");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = messageInput.value.trim();
      if (!text) return;
      respDiv.textContent = "Thinking…";
      const button = form.querySelector("button");
      button.disabled = true;
      try {
        const res = await fetch("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        if (res.ok) {
          respDiv.textContent = data.reply ?? "[no reply]";
        } else {
          respDiv.textContent = "Error: " + (data.error || res.statusText);
        }
      } catch (err) {
        respDiv.textContent = "Network error: " + err;
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
"""

# === ROUTES ===
@app.route("/", methods=["GET", "HEAD"])
def index():
    if request.method == "HEAD":
        return "", 200
    return Response(HTML_PAGE, mimetype="text/html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400

    message = data["message"]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}],
            max_tokens=256,
        )
        answer = response.choices[0].message.content
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === START APP ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
