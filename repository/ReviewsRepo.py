import psycopg2
from models.Reviews import Reviews

def db_conn():
    url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
    return psycopg2.connect(url)

def add_review(customer_name, book_name, description, rating):
    try:
        connection = db_conn()
        cursor = connection.cursor()

        cursor.execute('''BEGIN TRANSACTION''')
        cursor.execute('''SELECT "CustomerID" FROM public."Customer" WHERE "CustomerName" = %s''', (customer_name,))
        customer_id = cursor.fetchone()
        if customer_id:
            customer_id = customer_id[0]
        else:
            raise ValueError("There is no such customer")
        cursor.execute('''SELECT "BookID" FROM public."Book" WHERE "BookName" = %s''', (book_name,))
        book_id = cursor.fetchone()
        if book_id:
            book_id = book_id[0]
        else:
            raise ValueError("There is no such book")
        cursor.execute('''SELECT MAX("ReviewsID") FROM public."Reviews"''')
        reviews_id = cursor.fetchone()[0] + 1

        cursor.execute('''INSERT INTO public."Reviews"("ReviewsID", "CustomerID", "BookID", "Description", "Rating") VALUES (%s, %s, %s, %s, %s)''', (reviews_id, customer_id, book_id, description, rating))
        connection.commit()
        return True, None
    except Exception as e:
        if connection:
            connection.rollback()
        return False, str(e)
    finally:
        if connection:
            cursor.close()
            connection.close()