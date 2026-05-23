#!/usr/bin/env python3
"""
server.py — Local proxy server for LLM Security Scanner
Bridges the browser frontend with the Anthropic API.

Usage:
    pip install flask anthropic flask-cors
    export ANTHROPIC_API_KEY=your_key_here
    python server.py

Then open: http://localhost:5000
"""

import os
import json
import anthropic
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

PROMPT_TEMPLATE = """You are a security analyst. Analyze this Python code for security vulnerabilities.

Return ONLY a raw JSON array. No markdown, no explanation, no backticks. Just the JSON array.

Each object must have exactly these fields:
- "type": short name (e.g. "Command Injection")
- "severity": one of "HIGH", "MEDIUM", "LOW"
- "line": line number as integer (best estimate)
- "problem": one sentence describing the specific risk
- "fix": one sentence describing the recommended fix

Code:
{code}"""


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    code = data.get("code", "").strip()

    if not code:
        return jsonify({"error": "No code provided"}), 400

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY not set"}), 500

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": PROMPT_TEMPLATE.format(code=code)
                }
            ]
        )

        raw = message.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        issues = json.loads(raw)

        return jsonify({"issues": issues})

    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse Claude response"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n❌ Error: ANTHROPIC_API_KEY is not set.")
        print("   Run: export ANTHROPIC_API_KEY=your_key_here\n")
    else:
        print("\n✅ LLM Security Scanner server starting...")
        print("   Open your browser at: http://localhost:5000\n")

    app.run(debug=False, port=5000)
