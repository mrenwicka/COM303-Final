import mysql.connector
from mysql.connector import Error

###################################################################################################################


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Jabooze_31',
            database='homedepot'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

#excuting SQL queries
def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        return cursor
    except Error as e:
        print(f"Error: {e}")
        return None

#-------------------------------------------------------------------------------------------------------------#

# 1. What are the 20 top-selling products at each store?
def query_1():
    connection = create_connection()
    if connection:
        query = """
        SELECT 
            s.store_id,
            s.storeAddress,
            p.productName,
            SUM(oi.quantity) AS total_sold
        FROM 
            Store s
        JOIN 
            Orders o ON s.store_id = o.store_id
        JOIN 
            OrderItems oi ON o.order_id = oi.order_id
        JOIN 
            Products p ON oi.product_id = p.product_id
        GROUP BY 
            s.store_id, p.product_id
        ORDER BY 
            s.store_id ASC, total_sold DESC
        LIMIT 20;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            for result in results:
                print(f"Store ID: {result[0]}, Address: {result[1]}, Product: {result[2]}, Total Sold: {result[3]}")
        connection.close()
    else:
        print("Connection failed.")

# 2. What are the top 5 customers with the most purchases?
def query_2():
    connection = create_connection()
    if connection:
        query = """
        SELECT 
            c.customer_id,
            c.customerName,
            COUNT(o.order_id) AS PurchaseCount
        FROM 
            Customer c
        JOIN 
            Orders o ON c.customer_id = o.customer_id
        GROUP BY 
            c.customer_id, c.customerName
        ORDER BY 
            PurchaseCount DESC
        LIMIT 5;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            for result in results:
                print(f"Customer ID: {result[0]}, Name: {result[1]}, Purchases: {result[2]}")
        connection.close()
    else:
        print("Connection failed.")

# 3. What are the 5 most profitable stores?
def query_3():
    connection = create_connection()
    if connection:
        query = """
        SELECT 
            s.store_id,
            s.storeAddress,
            SUM(o.totalPrice) AS TotalRevenue
        FROM 
            Store s
        JOIN 
            Orders o ON s.store_id = o.store_id
        GROUP BY 
            s.store_id, s.storeAddress
        ORDER BY 
            TotalRevenue DESC
        LIMIT 5;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            for result in results:
                print(f"Store ID: {result[0]}, Address: {result[1]}, Total Revenue: ${result[2]:,.2f}")
        connection.close()
    else:
        print("Connection failed.")

# 4. In how many stores does DeWalt outsell Milwaukee?
def query_4():
    connection = create_connection()
    if connection:
        query = """
        SELECT 
            COUNT(DISTINCT store_id) AS stores_where_dewalt_outsells_milwaukee
        FROM (
            SELECT 
                s.store_id,
                SUM(CASE WHEN p.brand_id = 1 THEN oi.quantity ELSE 0 END) AS dewalt_sold,
                SUM(CASE WHEN p.brand_id = 2 THEN oi.quantity ELSE 0 END) AS milwaukee_sold
            FROM 
                Store s
            JOIN 
                Orders o ON s.store_id = o.store_id
            JOIN 
                OrderItems oi ON o.order_id = oi.order_id
            JOIN 
                Products p ON oi.product_id = p.product_id
            WHERE 
                p.brand_id IN (1, 2) -- 1 = DeWalt, 2 = Milwaukee
            GROUP BY 
                s.store_id
            HAVING 
                dewalt_sold > milwaukee_sold
        ) AS temp;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchone()
            print(f"Number of stores where DeWalt outsells Milwaukee: {results[0]}")
        connection.close()
    else:
        print("Connection failed.")

# 5. What are the top 3 types of product that customers buy in addition to DeWalt products?
def query_5():
    connection = create_connection()
    if connection:
        query = """
        SELECT 
            pt.productTypeName,
            COUNT(DISTINCT oi2.product_id) AS co_purchase_count
        FROM 
            OrderItems oi1
        JOIN 
            OrderItems oi2 ON oi1.order_id = oi2.order_id
        JOIN 
            Products p1 ON oi1.product_id = p1.product_id
        JOIN 
            Products p2 ON oi2.product_id = p2.product_id
        JOIN 
            ProductType pt ON p2.productType_id = pt.productType_id
        WHERE 
            p1.brand_id = 1 -- DeWalt
            AND p2.product_id != p1.product_id -- Not the same product
        GROUP BY 
            pt.productType_id
        ORDER BY 
            co_purchase_count DESC
        LIMIT 3;
        """
        cursor = execute_query(connection, query)
        if cursor:
            results = cursor.fetchall()
            if results:
                for result in results:
                    print(f"Product Type: {result[0]} -- Total Co-Purchases: {result[1]}")
            else:
                print("No additional products found purchased with DeWalt products.")
        connection.close()
    else:
        print("Connection failed.")


#run function to test queries
def Test_Queries():
    print("\n20 top-selling products at each store")
    query_1()
    print("\n20 top-selling products in each state")
    query_2()
    print("\n5 stores with the most sales so far this year")
    query_3()
    print("\nStores where DeWalt outsell Milwaukee")
    query_4()
    print("\nTop 3 types of product that customers buy in addition to DeWalt products")
    query_5()
    MainMenu()


###################################################################################################################

def DB_Admin():
    print("\n-----------------------------------------\n DBA Home Page \n Please select:")
    print(" 1. Run sales queries")
    print(" 2. Run OLAP queries")
    print(" 3. Main Menu")
    choice = int(input())
    if choice == 1:
        Test_Queries()
    elif choice == 2:
        query = input("Enter the OLAP query: ")
        self.run_olaps(query)
    elif choice == 3:
        MainMenu()
    else:
        print("Please select one of the above options.")

def run_olaps(self, query):
        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
        finally:
            self.close_connection()

def MainMenu():
    print("\n----------------------------------------\n")
    print("Welcome to Home Depots Online Store!")
    print("Please select one of the following:")
    print("1. Database Administrator")
    print("2. Warehouse Manager")
    print("3. Customer")
    choice_2 = int(input())
    if choice_2 == 1:
        DB_Admin()
    elif choice_2 == 2:
        WarehouseMenu()
    elif choice_2 == 3:
        CustomerMenu()
    else:
        print("Please select one of the above options.")

def CustomerMenu():
    connection = create_connection()
    if not connection:
        print("Connection failed.")
        return

    cart = [] 

    while True:
        print("\n--- Customer Menu ---")
        print("1. View Products")
        print("2. Add Product to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. Return to Main Menu")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1: #View Products
            #products wiht store 
            query = """
            SELECT 
                pp.product_id, p.productName, s.store_id, s.storeAddress, pp.priceDecimal
            FROM 
                ProductPricing pp
            JOIN 
                Products p ON pp.product_id = p.product_id
            JOIN 
                Store s ON pp.store_id = s.store_id
            ORDER BY 
                p.productName ASC, s.store_id ASC;
            """
            cursor = execute_query(connection, query)
            products = cursor.fetchall()
            print("\nAvailable Products by Store:")
            for product in products:
                print(f"Product ID: {product[0]}, Name: {product[1]}, Store ID: {product[2]}, Store Address: {product[3]}, Price: ${product[4]:,.2f}")
        
        elif choice == 2: #Add Product to Cart
            product_id = int(input("Enter Product ID to add to cart: "))
            store_id = int(input("Enter Store ID: "))
            quantity = int(input("Enter quantity: "))
        
            # Check if product is in inventory at that store
            cursor = execute_query(connection, """
                SELECT quantity FROM Inventory
                WHERE product_id = %s AND store_id = %s
            """, (product_id, store_id))
            result = cursor.fetchone()
        
            if not result:
                print(f"This product is not available at Store ID {store_id}.")
            elif result[0] < quantity:
                print(f"Only {result[0]} units available in stock. Cannot add {quantity}.")
            else:
                cart.append((product_id, store_id, quantity))
                print("Product added to cart.")

        
        elif choice == 3: #View Cart
            if cart:
                print("\nYour Cart:")
                for item in cart:
                    print(f"Product ID: {item[0]}, Store ID: {item[1]}, Quantity: {item[2]}")
            else:
                print("Cart is empty.")
        
        elif choice == 4: #Checkout
            if not cart:
                print("🛒 Cart is empty. Cannot checkout.")
                continue
        
            customer_id = int(input("Enter your Customer ID to place order: "))
        
            try:
                # Group cart items by store
                store_carts = {}
                for product_id, store_id, quantity in cart:
                    if store_id not in store_carts:
                        store_carts[store_id] = []
                    store_carts[store_id].append((product_id, quantity))
        
                for store_id, items in store_carts.items():
                    total_price = 0
                    for product_id, quantity in items:
                        cursor = execute_query(connection, """
                            SELECT priceDecimal FROM ProductPricing
                            WHERE product_id = %s AND store_id = %s
                        """, (product_id, store_id))
                        price_result = cursor.fetchone()
                        if price_result and price_result[0] is not None:
                            total_price += price_result[0] * quantity
                        else:
                            print(f"⚠Product {product_id} not available at Store {store_id}. Skipping.")
        
                    if total_price == 0:
                        print(f"No valid items for Store {store_id}. Skipping.")
                        continue
        
                    # Generate next order_id
                    cursor = execute_query(connection, "SELECT MAX(order_id) FROM Orders;")
                    max_order_id = cursor.fetchone()[0]
                    next_order_id = 1 if max_order_id is None else max_order_id + 1
        
                    # Insert into Orders
                    cursor = connection.cursor()
                    insert_order = """
                    INSERT INTO Orders (order_id, customer_id, store_id, orderDate, totalPrice)
                    VALUES (%s, %s, %s, NOW(), %s)
                    """
                    cursor.execute(insert_order, (next_order_id, customer_id, store_id, total_price))
        
                    # Insert OrderItems and subtract inventory
                    for product_id, quantity in items:
                        insert_order_item = """
                        INSERT INTO OrderItems (order_id, product_id, quantity)
                        VALUES (%s, %s, %s)
                        """
                        cursor.execute(insert_order_item, (next_order_id, product_id, quantity))
        
                        update_inventory = """
                        UPDATE Inventory
                        SET quantity = quantity - %s
                        WHERE store_id = %s AND product_id = %s
                        """
                        cursor.execute(update_inventory, (quantity, store_id, product_id))
        
                    print(f"\nOrder placed for Store {store_id}! Total: ${total_price:,.2f}")
        
                connection.commit()
        
            except Exception as e:
                print(f"An error occurred during checkout: {e}")
                connection.rollback()
            finally:
                cart.clear()

    
    
            
        elif choice == 5:
            connection.close()
            MainMenu()
            break
        
        else:
            print("Please select a valid option.")


def WarehouseMenu():
    while True:
        print("\n--- Warehouse Manager Menu ---")
        print("1. Generate Reorders (Check inventory levels)")
        print("2. Fulfill Reorders (Enter delivery info)")
        print("3. Record Shipment Inventory")
        print("4. Return to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            generate_reorders()
        elif choice == 2:
            fulfill_reorders()
        elif choice == 3:
            record_shipment_inventory()
        elif choice == 4:
            MainMenu()
            break
        else:
            print("Invalid option. Please select 1–4.")

def generate_reorders():
    connection = create_connection()
    if not connection:
        print("Connection failed.")
        return

    try:
        query = """
        INSERT INTO ReorderRequests (product_id, requestedQuantity, requestedDate, status)
        SELECT 
            i.product_id,
            100,  -- default reorder quantity
            NOW(),
            'Pending'
        FROM 
            Inventory i
        JOIN 
            ReorderThresholds rt ON i.product_id = rt.product_id
        WHERE 
            i.quantity < rt.threshold
            AND i.product_id NOT IN (
                SELECT product_id FROM ReorderRequests WHERE status = 'Pending'
            )
        """
        cursor = execute_query(connection, query)
        connection.commit()
        print("Reorder requests generated successfully (if needed).")
    except Exception as e:
        print(f"Error during reorder generation: {e}")
        connection.rollback()
    finally:
        connection.close()

def fulfill_reorders():
    connection = create_connection()
    if not connection:
        print("Connection failed.")
        return

    try:
        # Get all pending reorders
        query = """
        SELECT r.reorder_id, r.product_id, r.requestedQuantity
        FROM ReorderRequests r
        WHERE r.status = 'Pending'
        """
        cursor = execute_query(connection, query)
        pending = cursor.fetchall()

        if not pending:
            print("No pending reorders to fulfill.")
            return

        for reorder_id, product_id, quantity in pending:
            print(f"Fulfilling reorder ID {reorder_id} for product {product_id}, quantity {quantity}")
            warehouse_id = int(input("Enter fulfilling warehouse ID: "))

            insert_fulfillment = """
            INSERT INTO ReorderFulfillments (reorder_id, warehouse_id, deliveryDate, quantityReceived)
            VALUES (%s, %s, NOW(), %s)
            """
            cursor.execute(insert_fulfillment, (reorder_id, warehouse_id, quantity))

            update_status = """
            UPDATE ReorderRequests SET status = 'Fulfilled' WHERE reorder_id = %s
            """
            cursor.execute(update_status, (reorder_id,))

        connection.commit()
        print("All pending reorder requests fulfilled.")

    except Exception as e:
        print(f"Error during fulfillment: {e}")
        connection.rollback()
    finally:
        connection.close()


def record_shipment_inventory():
    connection = create_connection()
    if not connection:
        print("Connection failed.")
        return

    try:
        #fufillment reorders and requests
        query = """
        SELECT rf.reorder_id, rr.product_id, rf.quantityReceived
        FROM ReorderFulfillments rf
        JOIN ReorderRequests rr ON rf.reorder_id = rr.reorder_id
        WHERE rr.status = 'Fulfilled'
        """
        cursor = execute_query(connection, query)
        results = cursor.fetchall()

        if not results:
            print("No fulfilled shipments to apply.")
            return

        for reorder_id, product_id, qty in results:
            #cheking whcih store it is being delivered to
            store_id = int(input(f"Enter the Store ID receiving Product {product_id}: "))

            #if inventory exists
            check = execute_query(connection, """
                SELECT quantity FROM Inventory
                WHERE product_id = %s AND store_id = %s
            """, (product_id, store_id))
            row = check.fetchone()

            if row:
                #inventory update
                update = """
                UPDATE Inventory
                SET quantity = quantity + %s
                WHERE product_id = %s AND store_id = %s
                """
                execute_query(connection, update, (qty, product_id, store_id))
            else:
                #inserting new inventory record
                insert = """
                INSERT INTO Inventory (store_id, product_id, quantity)
                VALUES (%s, %s, %s)
                """
                execute_query(connection, insert, (store_id, product_id, qty))

            #marking reorder request as applied
            execute_query(connection, """
                UPDATE ReorderRequests SET status = 'Applied'
                WHERE reorder_id = %s
            """, (reorder_id,))

        connection.commit()
        print("Inventory successfully updated for all fulfilled shipments.")

    except Exception as e:
        print(f"Error while recording inventory: {e}")
        connection.rollback()
    finally:
        connection.close()


MainMenu()


        
