from flask import Flask, render_template, request, jsonify
import json
import os
import openai

app = Flask(__name__)

# Load config
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
    
    # Basic system prompt for the DM
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