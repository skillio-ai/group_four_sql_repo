from faker import Faker
from populate_data.config import config
import psycopg2
import random
from datetime import timedelta

fake = Faker()
Faker.seed(333)

def clean_database(con: psycopg2.extensions.connection):
    """
    Wipes the data so script can be re-run.
    """
    print("--- FRESH START: Cleaning database ---")
    # 'shipments' depends on 'orders', so we list it early (though CASCADE handles order)
    tables = ['shipments', 'order_items', 'orders', 'products', 'suppliers', 'customers']
    with con.cursor() as cur:
        for table in tables:
            cur.execute(f"TRUNCATE TABLE {table} CASCADE;")
    con.commit()

def populate_customers(con: psycopg2.extensions.connection, n: int):
    print(f'Populating {n} customers...')
    with con.cursor() as cur:
        for _ in range(n):
            cur.execute("""
                INSERT INTO customers (name, location, email) 
                VALUES (%s, %s, %s);
            """, (fake.name(), fake.city(), fake.unique.email()))
    con.commit()

def populate_suppliers(con: psycopg2.extensions.connection, n: int):
    print(f'Populating {n} suppliers...')
    with con.cursor() as cur:
        for _ in range(n):
            cur.execute("""
                INSERT INTO suppliers (name, contact_info, country)
                VALUES (%s, %s, %s)
            """, (fake.company(), fake.email(), fake.country()))
    con.commit()

def populate_products(con: psycopg2.extensions.connection, n: int):
    category_list = ['Electronics', 'Books', 'Clothing', 'Toys', 'Home']
    print(f'Populating {n} products...')
    with con.cursor() as cur:
        # Fetch supplier_ids
        cur.execute("SELECT supplier_id FROM suppliers;") 
        supplier_ids = [row[0] for row in cur.fetchall()]
        
        if not supplier_ids:
            print("Error: No suppliers found. Populate suppliers first.")
            return

        for _ in range(n):
            name = f"{fake.word().title()} {fake.word().title()}" 
            category = random.choice(category_list)
            price = round(random.uniform(10.00, 1000.00), 2)
            supplier_id = random.choice(supplier_ids)
            stock_quantity = random.randint(0, 100)

            cur.execute("""
                INSERT INTO products (name, category, price, supplier_id, stock_quantity) 
                VALUES (%s, %s, %s, %s, %s)
            """, (name, category, price, supplier_id, stock_quantity))
    con.commit()

def populate_orders(con: psycopg2.extensions.connection, n: int):
    """ 
    Populates orders.
    """
    print(f'Populating {n} orders...')
    
    statuses = ['pending', 'shipped', 'delivered']

    with con.cursor() as cur:
        # Fetch valid customer_ids
        cur.execute("SELECT customer_id FROM customers;")
        customer_ids = [row[0] for row in cur.fetchall()]

        if not customer_ids:
            print("Error: No customers found. Populate customers first")
            return

        for _ in range(n):
            customer_id = random.choice(customer_ids)
            order_date = fake.date_between(start_date='-2y', end_date='today')
            order_status = random.choice(statuses)

            cur.execute("""
                INSERT INTO orders (customer_id, order_date, order_status) 
                VALUES (%s, %s, %s)
            """, (customer_id, order_date, order_status))
    con.commit()

def populate_order_items(con: psycopg2.extensions.connection):
    print("Populating order items...")
    with con.cursor() as cur:
        cur.execute("SELECT order_id FROM orders;")
        order_ids = [row[0] for row in cur.fetchall()]
        
        cur.execute("SELECT product_id, price FROM products;")
        products = cur.fetchall() 
        
        if not order_ids or not products:
            print("Error: Ensure Orders and Products tables are populated.")
            return

        for order_id in order_ids:
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, num_items)
            
            for prod_id, price in selected_products:
                quantity = random.randint(1, 3)
                
                cur.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) 
                    VALUES (%s, %s, %s, %s)
                """, (order_id, prod_id, quantity, price))
    con.commit()

def populate_shipments(con: psycopg2.extensions.connection):
    """ 
    Populates shipments.
    Only creates shipments for 'Shipped' or 'Delivered' orders.
    """
    print("Populating shipments...")
    with con.cursor() as cur:
        # Fetch only relevant orders
        cur.execute(""" 
            SELECT order_id, order_date
            FROM orders
            WHERE order_status IN ('shipped', 'delivered');
        """)
        valid_orders = cur.fetchall()

        if not valid_orders:
            print("Warning: No shipped orders found.")
            return

        for order_id, order_date in valid_orders:
            days_to_ship = random.randint(1, 3)
            shipped_date = order_date + timedelta(days=days_to_ship)
            days_to_deliver = random.randint(2, 10)
            delivery_date = shipped_date + timedelta(days=days_to_deliver)
            shipping_cost = round(random.uniform(5.00, 50.00), 2)

            cur.execute("""
                INSERT INTO shipments (order_id, shipped_date, delivery_date, shipping_cost)
                VALUES (%s, %s, %s, %s)
            """, (order_id, shipped_date, delivery_date, shipping_cost))
    con.commit()

def main(con: psycopg2.extensions.connection):
    try:
        if con:
            print("\n--- Connected to database ---")
            
            # 1. Clean old data
            clean_database(con)

            # 2. Populate Independent Tables
            populate_customers(con, 1000) 
            populate_suppliers(con, 20)
            
            # 3. Populate Dependent Tables
            populate_products(con, 1100)
            populate_orders(con, 1000)
            
            # 4. Populate Highly Dependent Tables
            populate_order_items(con)
            populate_shipments(con)
            
            print("Database population complete.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")