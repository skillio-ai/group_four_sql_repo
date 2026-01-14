def get_total_orders(con):
    with con.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM orders;")
        return cur.fetchone()[0]

def get_total_sales(con):
    with con.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(SUM(price_at_purchase * quantity), 0)
            FROM order_items;
        """)
        return cur.fetchone()[0]

def get_low_stock_count(con, threshold: int = 10):
    with con.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE stock_quantity < %s;
        """, (threshold,))
        return cur.fetchone()[0]