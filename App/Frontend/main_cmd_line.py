
from Frontend.cmd_line_utils import *
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
                domain.new_expense( request_date(), 
                                    request_concept(), 
                                    request_amount("expense"), 
                                    request_tag()
                )
            case 2:
                domain.new_income(  request_date(), 
                                    request_concept(), 
                                    request_amount("income"), 
                                    request_tag()
                )
            case 3:
                #TODO: Complete list
                pass
            case -1:
                print("Finishing app")
            case _:
                print(f"Invalid operator {op}")
    
    log[0]("Finishing with return code 0\n")
    exit(0)
