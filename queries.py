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
    pass

#4.2.2
def get_avg_order_value(con):
    pass

#4.2.3
def get_monthly_orders_and_sales(con):
    pass

#4.3.1
def get_order_value_with_customer_name(con):
    pass

#4.3.2
def get_top5_customer(con):
    pass

#4.3.3
def get_suppliers_with_products(con):
    pass

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