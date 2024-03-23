import sqlite3
from Backend.domain import *
from ..utils import log

DB_FILE_NAME = "Backend/myMoney.db"
INIT_TABLES_SQL = "Backend/tables.sql"
TAG_FILES = "Backend/tags.txt"


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
            except sqlite3.OperationalError as e:
                print("### Unknonw error during initalitzation => DONE")
                print(e)

    con.commit()
    con.close()

def list_expenses_by_month():
    con = sqlite3.connect(DB_FILE_NAME)
    cursor = con.cursor()
    for row in cursor.execute("SELECT * FROM MonthlyExpensesWithTags "):
        print(row)
    con.close
    return

def list_tags():
    con = sqlite3.connect(DB_FILE_NAME)
    cursor = con.cursor()
    ret = {row[1] : row[0] for row in cursor.execute("SELECT * FROM TAGS")}
    con.close
    return ret

def add_movement(m: Movement):
    con = sqlite3.connect(DB_FILE_NAME)
    cursor = con.cursor()
    cursor.execute(f"INSERT INTO movements VALUES (NULL, {movent_to_txt(m)})")
    con.commit()
    con.close()

initialize_tables()