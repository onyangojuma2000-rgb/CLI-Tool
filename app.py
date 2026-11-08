from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
import os
# Load environment  variables
load_dotenv()
app = Flask(__name__)

# Get Anthropic API key
api_key = os.getenv("ANTHROPIC_API_KEY")

#Initialize Claude client
client = Anthropic(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process_text():
    try:
        # Check whether the API key is configured
        if client is None:
            return jsonify({
                "error": "AI service is not configured. Please add your API key."
            }), 500

        # Get submitted text
        data = request.get_json(silent=True) or {}
        user_text = data.get("text", "").strip()

        # Validate input
        if not user_text:
            return jsonify({
                "error": "Please enter some text."
            }), 400

        # Send text to Claude Haiku 4.5
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        # Extract Claude's response
        result = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        return jsonify({
            "result": result
        })

    except Exception:
        app.logger.exception("Text processing failed")
        return jsonify({
            "error": "Unable to process your text. Please try again."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)