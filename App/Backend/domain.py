from dataclasses import dataclass
from datetime import datetime
from utils import log

@dataclass
class Movement:
    date : datetime
    amount : float
    concept : str
    tag : str

    def __str__(self) -> str:
        return f"\"{self.date}\", \"{self.concept}\", {self.amount}, {self.tag}"    


# ======= Tx create expense =======

def new_expense(date : datetime, concept : str, amount : float, tag : str):
    log[0]("Creating expense with ...\n")

    if amount > 0:
        log[1]("Positive expense, converting into negative")
        amount = amount * -1

    if amount == 0:
        log[1]("Empty expense, amount == 0")

    m = Movement(date, amount, concept, tag)


# ======= Tx create income =======

def new_income(date : datetime, concept : str, amount : float, tag : str):
    log[0]("Creating income with ...\n")

    if amount == 0:
        log[1]("Empty expense, amount == 0")

    m = Movement(date, amount, concept, tag)