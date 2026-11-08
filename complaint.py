import os
from anthropic import Anthropic
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024

SYSTEM_PROMPT =  """You are a customer-support writing assistant for small businesses.
Write a ready-to-send reply to the customer's complaint.
Be polite, calm, professional, and empathetic. Acknowledge the specific issue.
Apologise for the frustrating experience where appropriate. Offer one clear,
realistic next step. Do not blame anyone. Do not invent facts, compensation,
refunds, delivery dates, or completed actions. Do not make unconfirmed promises.
Keep the reply concise (about 60–110 words). Return only the draft.
"""

def generate_reply(complaint):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("AI service is not configured. Add ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")

    response = client.messages.create(
        model=model,
        max_tokens=250,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Customer complaint:\n{complaint}"}
        ],
    )

    reply = "".join(
        block.text for block in response.content
        if getattr(block, "type", "") == "text"
    ).strip()

    if not reply:
        raise RuntimeError("The AI service returned an empty reply.")

    return reply


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    complaint = data.get("complaint", "")

    if not isinstance(complaint, str) or not complaint.strip():
        return jsonify({
            "error": "Please enter the customer's complaint."
        }), 400

    complaint = complaint.strip()

    if len(complaint) > 5000:
        return jsonify({
            "error": "Please keep the complaint under 5,000 characters."
        }), 400

    try:
        return jsonify({"reply": generate_reply(complaint)})
    except Exception:
        app.logger.exception("Reply generation failed")
        return jsonify({
            "error": "A reply could not be generated. Check the AI API configuration and try again."
        }), 502


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({
        "error": "The submitted message is too large."
    }), 413


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        debug=False
    )