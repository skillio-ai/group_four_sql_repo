#analytical queries
#4.1.1
def get_total_orders(con):
    with con.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM orders;")
        return cur.fetchone()[0]

#4.1.2
def get_total_sales(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(SUM(price_at_purchase * quantity), 0)
            FROM order_items;
        """)
        return cur.fetchone()[0]

#4.1.3
def get_low_stock_count(con, threshold: int = 10):
    with con.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE stock_quantity < %s;
        """, (threshold,))
        return cur.fetchone()[0]
    
#4.2.1
def get_total_sales_per_product(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT p.category AS category_, SUM(oi.price_at_purchase * oi.quantity) AS total_sales
            FROM order_items AS oi
            JOIN products AS p ON p.product_id = oi.product_id
            GROUP BY p.category
            ORDER BY total_sales DESC;
        """)
        return cur.fetchall()

#4.2.2
def get_avg_order_value(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT SUM(oi.price_at_purchase * oi.quantity)/COUNT(DISTINCT orders.order_id) average_order_value
            FROM orders
            JOIN order_items AS oi ON oi.order_id = orders.order_id;
        """)
        return cur.fetchall()

#4.2.3
def get_monthly_orders_and_sales(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT DATE_TRUNC('month',orders.order_date) AS month, COUNT(DISTINCT orders.order_id), COALESCE(SUM(oi.price_at_purchase * oi.quantity), 0) AS total_sales
            FROM orders
            JOIN order_items AS oi ON oi.order_id = orders.order_id
            GROUP BY month
            ORDER BY month;
        """)
        return cur.fetchall()

#4.3.1
def get_order_value_with_customer_name(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT orders.order_id, customers.name, SUM(oi.price_at_purchase * oi.quantity) AS sales
            FROM orders
            JOIN order_items AS oi ON oi.order_id = orders.order_id
            JOIN customers ON customers.customer_id = orders.customer_id
            GROUP BY orders.order_id, customers.name;
        """)
        return cur.fetchall()

#4.3.2
def get_top5_customer(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT customers.name AS name, SUM(oi.price_at_purchase * oi.quantity) as total_sales
            FROM customers
            JOIN orders ON orders.customer_id = customers.customer_id
            JOIN order_items AS oi ON oi.order_id = orders.order_id
            GROUP BY name
            ORDER BY total_sales DESC
            LIMIT 5;
        """)
        return cur.fetchall()

#4.3.3
def get_suppliers_with_products(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT suppliers.name, COUNT(products.product_id) AS product
            FROM suppliers
            JOIN products ON products.supplier_id = suppliers.supplier_id
            GROUP BY suppliers.supplier_id
            ORDER BY product DESC;
        """)
        return cur.fetchall()

#4.4.1
def get_poducts_not_sold(con):
    pass

#4.4.2
def get_customers_bought_above_treshold(con):
    pass

#4.4.3
def get_orders_most_products(con):
    pass

#4.5.1
def get_daily_orders_with_peak(con):
    pass

#4.5.2
def get_avg_monthly_deliverytime(con):
    pass

#4.5.3
def get_percentage_total_sales_from_top_products(con):
    pass