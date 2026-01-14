from populate_data.config import config
import populate_data.randomized_data
import psycopg2
from queries import *

def populate(con: psycopg2.extensions.connection):
    populate_data.randomized_data.main(con)

def menu_tree(con: psycopg2.extensions.connection):
    print("Give the choice for what you want to do.")
    print("  Choices:\n  ['populate'/'1']: populate the database\n  ['choices'/'2']: print choices again\n  ['end'/'0']: Terminate program")
    while True:

        choice = input("Pick: ").strip()

        if choice in ("populate", "1"):
            populate(con)
        elif choice in ("choices", "2"):
            print("  Choices:\n  ['populate'/'1']: populate the database\n  ['choices'/'2']: print choices again\n  ['end'/'0']: Terminate program")
        elif choice in ("total orders", "3"):
            temp=get_total_orders(con)
            print(temp)
        elif choice in ("total sales", "4"):
            temp=get_total_sales(con)
            print(temp)
        elif choice in ("get low stock", "5"):
            temp=get_low_stock_count(con)
            print(temp)
        elif choice in ("end", "0"):
            break
        else:
            print("Invalid choice")

def connect():
    return psycopg2.connect(**config())

def main():
    con = None
    try:
        con = connect()
        menu_tree(con)
    except Exception as e:
        print("Error:", e)
    finally:
        if con is not None:
            con.close()

if __name__ == "__main__":
    main()