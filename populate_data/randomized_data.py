from faker import Faker
from config import config
import psycopg2

fake = Faker()
Faker.seed(333)
def connect():
    return psycopg2.connect(**config())

def populate_customers(con: psycopg2.extensions.connection, n: int):
    with con.cursor() as cur:
        for _ in range(n):
            cur.execute("INSERT INTO customers (name, location, email) VALUES (%s, %s, %s);",
                        (fake.name(),fake.city(),fake.unique.email()))
    con.commit()

def print_customer(con: psycopg2.extensions.connection):
    with con.cursor() as cur:
        cur.execute("SELECT * FROM customers;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

def main():
    con = None
    try:
        con = connect()
        #print("Connected:", con.closed == 0)
        #print("DSN:", con.dsn)
        #populate_customers(con, 1000)
        #print_customer(con)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()

if __name__ == "__main__":
    main()