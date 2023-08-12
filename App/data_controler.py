import sqlite3
from collections import namedtuple

DB_FILE_NAME = "Backend/myMoney.db"
INIT_TABLES_SQL = "Backend/tables.sql"
TAG_FILES = "Backend/tags.txt"

Movement = namedtuple("movement", "date, amount, concept, tag")


def initialize_tables():
    con = sqlite3.connect(DB_FILE_NAME)
    cursor = con.cursor()
    with open(INIT_TABLES_SQL, mode="r") as f:
        queries = f.read().split(";")
        for i, q in enumerate(queries[:-1]):
            print(f"DB: Initializing {i+1}/{len(queries)-1} ", end="")
        
            try:
                cursor.execute(q)
                print(f"=> DONE")
            except sqlite3.IntegrityError:
                print("... already in the system => DONE")
            except:
                print("##Unknonw error => ABORT")

    con.commit()
    con.close()


def add_expense(m: Movement):
    if m.amount > 0:
        raise ValueError("**Expense must have negative amount €")

def add_income(m: Movement):
    if m.amount < 0:
        raise ValueError("**Income must have positive amount €")


initialize_tables()