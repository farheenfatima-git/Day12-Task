import pandas as pd

transactions = pd.read_csv("sample_data.csv")
customers = pd.read_csv("customers.csv")


def total_expenses():
    return transactions[
        transactions["type"] == "expense"
    ]["amount"].sum()


def highest_expense_category():
    expenses = transactions[
        transactions["type"] == "expense"
    ]

    result = expenses.groupby("category")["amount"].sum()

    return result.idxmax(), result.max()


def customer_balance(customer):
    result = customers[
        customers["customer"].str.lower() == customer.lower()
    ]

    if result.empty:
        return None

    return result.iloc[0]["balance"]


def customers_above_balance(amount):
    result = customers[
        customers["balance"] > amount
    ]

    return result.to_dict("records")