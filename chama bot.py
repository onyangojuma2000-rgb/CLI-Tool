
import os
import sys
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("ERROR: ANTHROPIC_API_KEY is missing from your .env file.")
    sys.exit(1)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)


# CHAMA KNOWLEDGE BASE
KNOWLEDGE_BASE = """
CHAMA NAME: Upendo Chama

1. MEMBERSHIP
- The chama has 20 registered members.
- New members must be approved by the committee.
- Members must provide their full name and contact details.

2. CONTRIBUTIONS
- Every member contributes KES 2,000 per month.
- Contributions are due on or before the 5th of each month.
- Payments are made through the chama treasurer.
- Members should retain payment confirmation.

3. MEETINGS
- Meetings are held on the first Saturday of every month.
- Meeting time is 10:00 AM.
- Meetings take place at the chama chairperson's office.
- Members should inform the secretary if they cannot attend.

4. FINES
- Late monthly contributions attract a KES 200 fine.
- Missing a meeting without informing the secretary attracts
  a KES 100 fine.
- Members may contact the committee if they dispute a fine.

5. LOANS
- A member must have contributed for at least three months
  before applying for a loan.
- Loan approval depends on available chama funds and committee
  approval.
- The maximum loan is KES 20,000.
- The interest rate is 5% per month.
- Repayment period is three months.

6. SAVINGS AND WITHDRAWALS
- Members can request withdrawal of their savings by writing
  to the committee.
- Withdrawal requests require committee approval.
- Processing takes up to 14 days after approval.

7. LEADERSHIP
- The chairperson leads chama meetings.
- The secretary keeps records and communicates with members.
- The treasurer manages contributions and financial records.

IMPORTANT RULES:
- Answer using only the information in this knowledge base.
- Do not invent policies, amounts, dates or decisions.
- If information is unavailable, say:
  "I do not have that information. Please confirm with the
  chama secretary or committee."
- Give clear, short and polite answers.
- Do not claim that a loan, withdrawal or membership application
  has been approved.
"""


# SYSTEM PROMPT
SYSTEM_PROMPT = f"""
You are the official FAQ assistant for Upendo Chama.

Your job is to help the chama secretary answer members'
questions using the knowledge base below.

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

INSTRUCTIONS:
1. Answer questions using only the knowledge base.
2. Keep answers simple, clear and professional.
3. Include relevant amounts, dates and conditions.
4. Never invent missing information.
5. If a question is outside the knowledge base, direct the
   member to the secretary or committee.
6. Do not make financial decisions or approve loans.
7. If a question is unclear, ask for clarification.
"""


def ask_chama_bot(question):
    """Answer a member's question using Claude Haiku 4.5."""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

    except anthropic.AuthenticationError:
        return "Authentication error. Please check your Anthropic API key."

    except anthropic.APIConnectionError:
        return "Connection error. Check your internet connection."

    except anthropic.APIStatusError as error:
        return f"Anthropic API error: {error.status_code}"

    except Exception as error:
        return f"Unexpected error: {error}"


# EIGHT TEST QUESTIONS
TEST_QUESTIONS = [
    "How much should each member contribute monthly?",
    "When is the next chama meeting?",
    "What happens if I pay my contribution late?",
    "How much is the fine for missing a meeting?",
    "What are the requirements for getting a loan?",
    "What is the maximum loan amount?",
    "How can I withdraw my savings?",
    "How can someone become a member?"
]


def run_tests():
    """Test the bot using eight different question types."""

    print("\nUPENDO CHAMA FAQ BOT - TEST MODE")
    print("=" * 45)

    for number, question in enumerate(TEST_QUESTIONS, start=1):
        print(f"\nTEST {number}: {question}")

        answer = ask_chama_bot(question)

        print("BOT:", answer)
        print("-" * 45)


def main():
    print("\nWELCOME TO UPENDO CHAMA FAQ BOT")
    print("Ask questions about chama rules and operations.")
    print("Type /test to run eight test questions.")
    print("Type /quit to exit.")
    print("=" * 45)

    while True:
        question = input("\nSecretary: ").strip()

        if question.lower() == "/quit":
            print("Chama FAQ Bot closed.")
            break

        elif question.lower() == "/test":
            run_tests()

        elif not question:
            print("Please enter a question.")

        else:
            answer = ask_chama_bot(question)
            print("\nChama Bot:", answer)


if __name__ == "__main__":
    main()
