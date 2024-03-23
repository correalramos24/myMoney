
from Frontend.arguments import *
from datetime import datetime as dt
from utils import log, setLogging
from Backend import domain

def main():
    setLogging(True)
    # Initialize app
    # data.initialize_tables()

    op = 0
    while op != -1: 

        # Print options && do requested action
        print(options)
        op = int(input("Enter action: "))

        match op:
            case 1:
                amount = float(input("Enter amount for the expense: "))
                date = dt.today()
            case 2:
                amount = float(input("Enter amount for the income: "))
                date = dt.today()
            case 3:
                print("")
            case -1:
                print("Finishing app")
            case _:
                print(f"Invalid operator {op}")
    
    log[0]("Finishing with return code 0\n")
    exit(0)
