from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, Any

from ai_service import process_financial_query
from database import (
    total_expenses,
    highest_expense_category,
    customer_balance,
    customers_above_balance
)

from database import (
    customers,
    total_expenses,
    highest_expense_category,
    customer_balance,
    customers_above_balance
)

app = FastAPI()


class QueryRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    question: str = Field(..., min_length=3, max_length=500)

class QueryResponse(BaseModel):
    answer: Optional[str] = None
    error: Optional[str] = None
    customers: Optional[list[dict[str, Any]]] = None


@app.get("/")
def home():
    return {"message": "HisabDo Financial Query API"}


@app.post("/financial-query")
def financial_query(request: QueryRequest) -> QueryResponse:
    user = customers[
        customers["customer_id"] == request.user_id
    ]

    if user.empty:
        return {
            "error": "Invalid user_id."
        }

    try:
        query = process_financial_query(request.question)

    except ValueError:
        return QueryResponse(
            error="The AI returned an invalid response."
        )

    except Exception:
        return QueryResponse(
            error="Unable to process the financial question. Please try again."
        )

    intent = query.get("intent")

    supported_intents = {
        "total_expenses",
        "highest_expense_category",
        "customer_balance",
        "customer_balance_filter"
    }

    if intent not in supported_intents:
        return QueryResponse(
            error="This type of financial query is not supported yet."
        )

    if intent == "total_expenses":

        total = total_expenses()

        return {
            "answer": f"Your total expenses are PKR {total}."
        }

    elif intent == "highest_expense_category":

        category, amount = highest_expense_category()

        return {
            "answer": f"Your highest expense category is {category} with PKR {amount}."
        }

    elif intent == "customer_balance":

        customer = query.get("customer")
        balance = customer_balance(customer)

        if balance is None:
            return {
                "answer": f"No customer named {customer} was found."
            }

        return {
            "answer": f"{customer} owes you PKR {balance}."
        }

    elif intent == "customer_balance_filter":

        amount = query.get("amount")
        result = customers_above_balance(amount)

        return {
            "answer": f"{len(result)} customers owe you more than PKR {amount}.",
            "customers": result
        }

    return {
        "answer": "Sorry, I don't understand that financial question yet."
    }