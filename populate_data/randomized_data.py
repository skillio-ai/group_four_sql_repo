from faker import Faker
from populate_data.config import config
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

def main(con: psycopg2.extensions.connection):
    #populate_customers(con)
    print("data populated")
    pass