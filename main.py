from populate_data.config import config
import psycopg2

def menu_tree(con: psycopg2.extensions.connection):
    print("Give the choice for what you want to do.")
    while True:
        print("Choices:\n'end': Terminate program\n'bla': run bla query")

        choice = input("Pick: ").strip()

        if choice == "end":
            break
        else:
            pass

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