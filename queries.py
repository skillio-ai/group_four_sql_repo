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
            GROUP BY orders.order_id, customers.name
            LIMIT 25;
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
def get_products_not_sold(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT products.name
            FROM products
            LEFT JOIN order_items ON order_items.product_id = products.product_id
            WHERE order_items.product_id IS NULL
            GROUP BY products.name
            LIMIT 20;
        """)
        return cur.fetchall()

#4.4.2
def get_customers_bought_above_threshold(con, threshold2: int = 1000):
    with con.cursor() as cur:
        cur.execute("""
            SELECT customers.name AS name, SUM(oi.price_at_purchase * oi.quantity) AS total_sales
            FROM customers
            JOIN orders ON orders.customer_id = customers.customer_id
            JOIN order_items AS oi ON oi.order_id = orders.order_id
            GROUP BY name
            HAVING SUM(oi.price_at_purchase * oi.quantity) > %s
            ORDER BY total_sales DESC
            LIMIT 25;
        """, (threshold2,))
        return cur.fetchall()

#4.4.3
def get_orders_most_products(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT orders.order_id, SUM(order_items.quantity) AS total_items
            FROM orders
            JOIN order_items ON order_items.order_id = orders.order_id
            GROUP BY orders.order_id
            ORDER BY total_items DESC
            LIMIT 5;
        """)
        return cur.fetchall()

#4.5.1
def get_daily_orders_with_peak(con):
    #daily orders ordered by most sales per day
    with con.cursor() as cur:
        cur.execute("""
            SELECT DATE_TRUNC('day', order_date) AS day, COUNT(order_id) as total_orders
            FROM orders
            GROUP BY day
            ORDER BY total_orders DESC
            LIMIT 5;     
        """)
        return cur.fetchall()

#4.5.2
def get_avg_monthly_deliverytime(con):
    #difference between orders.order_date and shipments.delivery_date
    #average of those, grouped by month
    with con.cursor() as cur:
        cur.execute("""
            SELECT DATE_TRUNC('month', shipped_date) AS month, AVG(DATE(delivery_date) - DATE(shipped_date)) AS average_delivery_time 
            FROM shipments
            GROUP BY month
            ORDER BY month DESC;     
        """)
        return cur.fetchall()

#4.5.3
def get_percentage_total_sales_from_top_products(con):
    #how much of the total sales have the top 10% of products brought in
    #group by products and order by each products sale
    with con.cursor() as cur:
        #/*---- add selects up, but limit them to only be 10% of products sold ---*/
        cur.execute("""
                WITH product_sales AS (SELECT p.name, SUM(oi.price_at_purchase * oi.quantity) AS total_sales 
                    FROM products AS p
                    JOIN order_items AS oi ON oi.product_id = p.product_id
                    GROUP BY p.name),
                    top_products AS (SELECT *, NTILE(10) OVER (ORDER BY total_sales DESC) AS revenue
                    FROM product_sales),
                    totals AS (SELECT SUM(total_sales) FROM product_sales)
                SELECT (SUM(CASE WHEN revenue = 1 THEN total_sales ELSE 0 END) / SUM(total_sales)) * 100 FROM top_products;
        """)
        return cur.fetchall()