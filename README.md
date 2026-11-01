# CLI-Tool
PYthon CLI tool that engages in interactive conversation/assisant bot using claude-haiku-4-5

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
