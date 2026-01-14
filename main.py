from populate_data.config import config
import populate_data.randomized_data
import psycopg2
import datetime as dt
from queries import *

def populate(con: psycopg2.extensions.connection):
    populate_data.randomized_data.main(con)

def print_choices():
    print("""  Choices:
    ['populate'/'1']: populate the database
    ['choices'/'2']: print choices again
    ['total orders'/'3']: get the total amount of orders
    ['total sales'/'4']: get the total sales
    ['get low stock'/'5']: get amount of products that have low stock
    ["sales per product"/ "6"]:
    ["avg order value"/ "7"]:
    ["monthly orders and sales"/ "8"]:
    ["order value customer"/ "9"]:
    ["top5 customer"/ "10"]:
    ["suppliers products"/ "11"]:
    ["bad poducts"/ "12"]:
    ["customers above treshold"/ "13"]:
    ["orders by products"/ "14"]:
    ["daily orders peak"/ "15"]:
    ["avg monthly deliverytime"/ "16"]:
    ["percentage sales products"/ "17"]:
    ['end'/'0']: Terminate program""")

def menu_tree(con: psycopg2.extensions.connection):
    print("Give the choice for what you want to do.")
    print_choices()
    while True:
        choice = input("Pick: ").strip()
        if choice in ("populate", "1"):
            populate(con)
        elif choice in ("choices", "2"):
            print_choices()
        elif choice in ("total orders", "3"):
            temp=get_total_orders(con)
            print(temp)
        elif choice in ("total sales", "4"):
            temp=get_total_sales(con)
            print(temp)
        elif choice in ("get low stock", "5"):
            temp=get_low_stock_count(con)
            print(temp)
        elif choice in ("sales per product", "6"):
            temp=get_total_sales_per_product(con)
            for n in temp:
                print(n[0],n[1])
        elif choice in ("avg order value", "7"):
            temp=get_avg_order_value(con)
            print(f"Average order value: {round(temp[0][0], 1)}")
        elif choice in ("monthly orders and sales", "8"):
            temp=get_monthly_orders_and_sales(con)
            for n in temp:
                print(f"Total orders and sales by year and month: {n[0].strftime('%Y.%m')}, orders {n[1]}, sales {n[2]}")
        elif choice in ("order value customer", "9"):
            temp=get_order_value_with_customer_name(con)
            for n in temp:
                print(f"Order: {n[0]} was made by {n[1]} for a total of {n[2]}")
        elif choice in ("top5 customer", "10"):
            temp=get_top5_customer(con)
            for n in temp:
                print(f"Customer: {n[0]} spent {n[1]}")
        elif choice in ("suppliers products", "11"):
            temp=get_suppliers_with_products(con)
            for n in temp:
                print(f"Supplier {n[0]} has {n[1]} products")
        elif choice in ("bad poducts", "12"):
            temp=get_poducts_not_sold(con)
            print(temp)
        elif choice in ("customers above treshold", "13"):
            temp=get_customers_bought_above_treshold(con)
            print(temp)
        elif choice in ("orders by products", "14"):
            temp=get_orders_most_products(con)
            print(temp)
        elif choice in ("daily orders peak", "15"):
            temp=get_daily_orders_with_peak(con)
            print(temp)
        elif choice in ("avg monthly deliverytime", "16"):
            temp=get_avg_monthly_deliverytime(con)
            print(temp)
        elif choice in ("percentage sales products", "17"):
            temp=get_percentage_total_sales_from_top_products(con)
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