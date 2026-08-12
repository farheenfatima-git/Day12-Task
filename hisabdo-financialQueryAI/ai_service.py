import os
import json
from dotenv import load_dotenv
from google import genai

SUPPORTED_INTENTS = {
    "total_expenses",
    "highest_expense_category",
    "customer_balance",
    "customer_balance_filter"
}

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def process_financial_query(question):

    prompt = f"""
You are a multilingual financial query parser.

The user may ask questions in:
- English
- Urdu
- Roman Urdu
- Mixed language

Convert the user's question into JSON.

Supported intents:
- total_expenses
- highest_expense_category
- customer_balance
- customer_balance_filter

Return ONLY valid JSON.

Examples:

Question: How much did I spend?
JSON: {{"intent": "total_expenses"}}

Question: Maine kitna kharcha kiya?
JSON: {{"intent": "total_expenses"}}

Question: Ali par kitne paise baqi hain?
JSON: {{"intent": "customer_balance", "customer": "Ali"}}

Question: How much does Ali owe me?
JSON: {{"intent": "customer_balance", "customer": "Ali"}}

Question: Who owes me more than PKR 20000?
JSON: {{"intent": "customer_balance_filter", "amount": 20000}}

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    try:
        result = json.loads(response.text.strip())

        if not isinstance(result, dict):
            raise ValueError("AI response is not a JSON object")

        if "intent" not in result:
            raise ValueError("AI response does not contain an intent")

        if result["intent"] not in SUPPORTED_INTENTS:
            raise ValueError("Unsupported financial intent")

        return result

    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Invalid AI response: {e}")