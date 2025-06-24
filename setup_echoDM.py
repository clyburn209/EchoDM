import os

# Define all file contents
files = {
    ".gitignore": """config.json
.env
__pycache__/
*.pyc
*.pyo
.DS_Store
""",

    "requirements.txt": """Flask==2.3.3
python-dotenv==1.0.1
requests==2.31.0
""",

    "config_template.json": """{
  "openai_key": "sk-...",
  "avrae_token": "Bot YOUR_AVRAE_DISCORD_BOT_TOKEN",
  "character_url": "https://ddb.ac/characters/your-character-id",
  "owlbear_url": "https://owlbear.rodeo/room-code"
}
""",

    "app.py": '''from flask import Flask, render_template, request, jsonify
import json
import openai

app = Flask(__name__)

with open("config.json") as f:
    config = json.load(f)

openai.api_key = config["openai_key"]

@app.route("/")
def index():
    return render_template("index.html",
                           character_url=config.get("character_url", ""),
                           owlbear_url=config.get("owlbear_url", ""))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    messages = [
        {"role": "system", "content": "You are the player's personal Dungeon Master. Respond narratively and request rolls when needed."},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    reply = response.choices[0].message["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
''',

    "templates/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EchoDM</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <div class="setup-panel">
            <h2>Setup</h2>
            <ul>
                <li><a href="{{ character_url }}" target="_blank">Character Sheet</a></li>
                <li><a href="{{ owlbear_url }}" target="_blank">Owlbear Map</a></li>
            </ul>
        </div>

        <div class="character-box">
            <h2>Character Info</h2>
            <p>(Eventually: parsed summary from D&D Beyond link)</p>
        </div>

        <div class="map-box">
            <iframe src="{{ owlbear_url }}" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <div class="chat-box">
            <div id="chatlog"></div>
            <textarea id="userInput" placeholder="Say something..."></textarea>
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById("userInput").value;
            const chatlog = document.getElementById("chatlog");
            chatlog.innerHTML += `<div class="user"><strong>You:</strong> ${input}</div>`;

            const response = await fetch("/chat", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input })
            });

            const data = await response.json();
            chatlog.innerHTML += `<div class="dm"><strong>EchoDM:</strong> ${data.reply}</div>`;
            document.getElementById("userInput").value = "";
            chatlog.scrollTop = chatlog.scrollHeight;
        }
    </script>
</body>
</html>
''',

    "static/style.css": '''body {
    font-family: sans-serif;
    margin: 0;
    padding: 0;
    background-color: #1d1f21;
    color: #e0e0e0;
}

.container {
    display: grid;
    grid-template-areas:
        "setup map"
        "character chat";
    grid-template-columns: 30% 70%;
    grid-template-rows: 40vh 60vh;
    height: 100vh;
    gap: 10px;
    padding: 10px;
}

.setup-panel {
    grid-area: setup;
    background: #2c2f33;
    padding: 10px;
}

.character-box {
    grid-area: character;
    background: #2c2f33;
    padding: 10px;
    overflow-y: auto;
}

.map-box {
    grid-area: map;
    background: #23272a;
}

.chat-box {
    grid-area: chat;
    background: #2c2f33;
    padding: 10px;
    display: flex;
    flex-direction: column;
}

#chatlog {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 10px;
}

textarea {
    width: 100%;
    height: 60px;
    background: #1d1f21;
    color: white;
    border: 1px solid #444;
    padding: 5px;
}

button {
    margin-top: 5px;
    padding: 10px;
    background-color: #7289da;
    border: none;
    color: white;
    cursor: pointer;
}
''',

    "README.md": '''# EchoDM 🎲

A solo D&D web interface powered by ChatGPT, Avrae, and Owlbear. Run immersive solo adventures with natural language narration, dynamic rolls, and map visualization.

## 🔧 Setup

1. Clone this repo
2. Copy `config_template.json` → `config.json` and fill in:
   - Your OpenAI key
   - Optional: Avrae bot token
   - Character sheet + Owlbear map URLs

3. Install dependencies:
```bash
pip install -r requirements.txt