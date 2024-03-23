
from datetime import datetime as dt

options = """
1. Enter expense
2. Enter income
3. List expenses/incomes
"""

def request_date():
    d = dt.date(dt.today())
    return d

def request_concept():
    concept = input("Enter concept: ")
    return concept

def request_amount(expense_or_income):
    amount = float(input(f"Enter amount for the : {expense_or_income}"))
    return amount

def request_tag():
    #TODO: Add list of available tags
    tag = input("Enter tag: ")
    return tag