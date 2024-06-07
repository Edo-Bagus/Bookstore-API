import psycopg2
from models.Wishlist import Wishlist  # Assuming Wishlist model is defined in models/Wishlist.py

# Function to establish a database connection
def db_conn():
    url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
    return psycopg2.connect(url)

# Function to add a book to a customer's wishlist
def add_wishlist(customer_name, book_name, store_name):
    try:
        connection = db_conn()
        cursor = connection.cursor()

        # Begin transaction
        cursor.execute('''BEGIN TRANSACTION''')

        # Retrieve CustomerID based on customer_name
        cursor.execute('''SELECT "CustomerID" FROM public."Customer" WHERE "CustomerName" = %s''', (customer_name,))
        customer_id = cursor.fetchone()

        if customer_id:
            customer_id = customer_id[0]  # Extract the CustomerID from the result
        else:
            raise ValueError("There is no such customer")

        # Retrieve BookID based on book_name
        cursor.execute('''SELECT "BookID" FROM public."Book" WHERE "BookName" = %s''', (book_name,))
        book_id = cursor.fetchone()

        if book_id:
            book_id = book_id[0]  # Extract the BookID from the result
        else:
            raise ValueError("There is no such book")

        # Retrieve StoreID based on store_name
        cursor.execute('''SELECT "StoreID" FROM public."Store" WHERE "StoreName" = %s''', (store_name,))
        store_id = cursor.fetchone()

        if store_id:
            store_id = store_id[0]  # Extract the StoreID from the result
        else:
            raise ValueError("There is no such store")

        # Generate a new WishlistID
        cursor.execute('''SELECT MAX("WishlistID") FROM public."Wishlist"''')
        wishlist_id = cursor.fetchone()[0] + 1  # Increment the maximum WishlistID

        # Check if the book is available in the specified store
        cursor.execute('''SELECT * FROM public."Store_Book" WHERE "Book_BookID" = %s AND "Store_StoreID" = %s''', (book_id, store_id))
        book_in_store = cursor.fetchone()

        if book_in_store:
            # Insert the book into the customer's wishlist
            cursor.execute('''INSERT INTO public."Wishlist"("WishlistID", "CustomerID", "BookID", "StoreID", "DateCreated") 
                              VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);''', (wishlist_id, customer_id, book_id, store_id))
        else:
            raise ValueError("Book is not in the store")

        # Commit the transaction
        connection.commit()
        return True, None
    except Exception as e:
        if connection:
            connection.rollback()  # Rollback the transaction if an exception occurs
        return False, str(e)
    finally:
        # Close cursor and connection
        if connection:
            cursor.close()
            connection.close()

