import psycopg2
from models.Book import Book  # Assuming Book model is defined in models/Book.py

# Function to establish a database connection
def db_conn():
    url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
    return psycopg2.connect(url)

# Function to retrieve all books from the database
def get_all_books():
    try:
        # Connect to database
        connection = db_conn()
        cursor = connection.cursor()
        
        # Query all books from the Book_View
        cursor.execute('''SELECT * FROM public."Book_View"''')
        data = cursor.fetchall()

        # Create Book objects from the retrieved data
        books = [Book(
            book_id=book[0],
            book_name=book[1],
            publication_year=book[2],
            pages=book[3],
            price=book[4],
            publisher_id=book[5],
            language_id=book[6],
            original_language_id=book[7]
        ) for book in data]
        
        return books, None
    except Exception as e:
        return [], str(e)
    finally:
        # Close connection to database
        if connection:
            cursor.close()
            connection.close()

# Function to retrieve books by a specific author
def get_books_by_author(author):
    try:
        connection = db_conn()
        cursor = connection.cursor()

        # Query books of a specific author
        cursor.execute('''
            SELECT * FROM public."Book_View"
            WHERE "BookID" IN (
                SELECT DISTINCT "BookID" 
                FROM public."Book_Author_Category_View" 
                WHERE "AuthorName" = %s
            );
        ''', (author,))
        data = cursor.fetchall()

        # Create Book objects from the retrieved data
        books = [Book(
            book_id=book[0],
            book_name=book[1],
            publication_year=book[2],
            pages=book[3],
            price=book[4],
            publisher_id=book[5],
            language_id=book[6],
            original_language_id=book[7]
        ) for book in data]

        if books:
            return books, None
        else:
            raise ValueError('Book is not found')
    except Exception as e:
        return [], str(e)
    finally:
        # Close connection to database
        if connection:
            cursor.close()
            connection.close()

# Function to delete books by name
def delete_books_by_name(book_name):
    try: 
        connection = db_conn()
        cursor = connection.cursor()

        # Begin transaction
        cursor.execute('''BEGIN TRANSACTION''')

        # Query to get book ID from book name
        cursor.execute('''SELECT "BookID" FROM public."Book" WHERE "BookName" = %s''', (book_name,))
        book_id = cursor.fetchone()

        # Check if the book exists
        if book_id:
            book_id = book_id[0]

            # Delete related entries from other tables
            cursor.execute('''DELETE FROM public."Store_Book" WHERE "Book_BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Category_Book" WHERE "Book_BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Book_Author" WHERE "Book_BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Wishlist" WHERE "BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Reviews" WHERE "BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Book" WHERE "BookID" = %s''', ((book_id,)))
        else:
            raise ValueError('Book not found')
        
        # Commit the transaction
        connection.commit()
        return True, None
    except Exception as e:
        if connection:
            connection.rollback() # Rollback the transaction if an exception occurs
        return False, str(e)
    finally:
        # Close connection to database
        if connection:
            cursor.close()
            connection.close()
