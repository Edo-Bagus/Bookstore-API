import psycopg2
from models.Book import Book

def db_conn():
    url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
    return psycopg2.connect(url)

def add_wishlist(customer_name, book_name, store_name):
    try: 
        connection = db_conn()
        cursor = connection.cursor()

        cursor.execute('''BEGIN TRANSACTION''')
        cursor.execute('''SELECT "CustomerID" FROM public."Customer" WHERE "CustomerName" = %s''', (customer_name,))
        customer_id = cursor.fetchone()[0]
        cursor.execute('''SELECT "BookID" FROM public."Book" WHERE "BookName" = %s''', (book_name,))
        book_id = cursor.fetchone()[0]
        cursor.execute('''SELECT "StoreID" FROM public."Store" WHERE "StoreName" = %s''', (store_name,))
        store_id = cursor.fetchone()[0]
        cursor.execute('''SELECT MAX("WishlistID") FROM public."Wishlist"''')
        wishlist_id = cursor.fetchone()[0] + 1

        cursor.execute('''SELECT * FROM public."Store_Book" WHERE "Book_BookID" = %s AND "Store_StoreID" = %s''', (book_id, store_id))
        book_in_store = cursor.fetchone()

        if book_in_store:
            cursor.execute('''INSERT INTO public."Wishlist"("WishlistID", "CustomerID", "BookID", "StoreID", "DateCreated") VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);''', (wishlist_id, customer_id, book_id, store_id))
        else:
            raise ValueError("Book is not in the store")
        
        connection.commit()
        return True
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error inserting wishlist: {str(e)}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()