**Upendo Chama FAQ Bot**

Answers chama members' questions about membership, contributions, meetings, fines, loans and savings using Claude Haiku 4.5 and a predefined knowledge base.

**Setup**

1. `pip install anthropic python-dotenv`
2. Create `.env` with: `ANTHROPIC_API_KEY=your-api-key`
3. Ensure `.env` is included in `.gitignore`.

**Usage**

Run the bot:

`python chama_bot.py`

Ask questions interactively, or enter `/test` to test eight different question types.

Enter `/quit` to exit.

**Features**
- Answers questions using the chama knowledge base.
- Provides information about contributions, meetings, fines and loans.
- Extracts relevant rules and conditions.
- Avoids inventing missing information.
- Includes API error handling.

**Cost**

API usage is charged according to Anthropic's Claude Haiku 4.5 pricing and the number of input and output tokens. Actual cost varies with question length and response size.
# Customer Complaint Reply Generator

**Live URL:** Add your Render URL here after deployment.

A web tool for Nairobi shops, restaurants, courier services, Airbnbs, and other small businesses. Paste a complaint, click **Generate Reply**, and receive a concise, professional draft on the same page.

## What it does

- Acknowledges the customer's specific concern.
- Uses a polite, calm, professional tone.
- Suggests a clear and realistic next step.
- Avoids blame, invented facts, and unconfirmed promises.
- Displays the result without reloading the page.

Review every draft and verify its facts before sending.

## Technology

Python, Flask, Anthropic Claude API, HTML, CSS, JavaScript Fetch API, and Gunicorn.

## Run locally (Windows PowerShell)

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
