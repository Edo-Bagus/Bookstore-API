import psycopg2
from models.Book import Book

def db_conn():
    url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
    return psycopg2.connect(url)

def get_all_books():
    try:
        connection = db_conn()
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM public."Book_View"''')
        data = cursor.fetchall()
        cursor.close()  
        connection.close()

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
        print(books)
        return books, None
    except Exception as e:
        return [], str(e)
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_books_by_author(author):
    try:
        connection = db_conn()
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM public."Book_View" WHERE "BookID" IN ( SELECT DISTINCT "BookID" FROM public."Book_Author_Category_View" WHERE "AuthorName" = %s);''', (author,))
        data = cursor.fetchall()

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
        if connection:
            cursor.close()
            connection.close()

def delete_books_by_name(name):
    try: 
        connection = db_conn()
        cursor = connection.cursor()

        cursor.execute('''BEGIN TRANSACTION''')
        cursor.execute('''SELECT "BookID" FROM public."Book" WHERE "BookName" = %s''', (name,))
        book_id = cursor.fetchone()
        if book_id:
            book_id = book_id[0]
            cursor.execute('''DELETE FROM public."Store_Book" WHERE "Book_BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Category_Book" WHERE "Book_BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Book_Author" WHERE "Book_BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Wishlist" WHERE "BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Reviews" WHERE "BookID" = %s''', ((book_id,)))
            cursor.execute('''DELETE FROM public."Book" WHERE "BookID" = %s''', ((book_id,)))
        else:
            raise ValueError('Book not found')
        
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


