import psycopg2
from models.Reviews import Reviews  # Assuming Reviews model is defined in models/Reviews.py

# Function to establish a database connection
def db_conn():
    url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
    return psycopg2.connect(url)

# Function to add a new review to the database
def add_review(customer_name, book_name, description, rating):
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

        # Generate a new ReviewsID
        cursor.execute('''SELECT MAX("ReviewsID") FROM public."Reviews"''')
        reviews_id = cursor.fetchone()[0] + 1  # Increment the maximum ReviewsID

        # Insert the new review into the Reviews table
        cursor.execute('''INSERT INTO public."Reviews"("ReviewsID", "CustomerID", "BookID", "Description", "Rating") 
                          VALUES (%s, %s, %s, %s, %s)''', (reviews_id, customer_id, book_id, description, rating))

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

def update_review(customer_name, book_name, description, rating):
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

         # Check if review exist between the customer and the book
        cursor.execute('''SELECT "ReviewsID" FROM public."Reviews" WHERE "CustomerID" = %s AND "BookID" = %s''', (customer_id, book_id))
        review_id = cursor.fetchone()

        if review_id:
            # Update the review
            review_id = review_id[0]
            cursor.execute('''UPDATE public."Reviews" 
                          SET "Description" = %s, "Rating" = %s 
                          WHERE "ReviewsID" = %s''', (description, rating, review_id))
        else:
            raise ValueError("The customer dont have any reviews about the book")
        
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