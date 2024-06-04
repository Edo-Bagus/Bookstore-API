import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

COUNT_BOOK = """SELECT COUNT(*) AS total_rows FROM public."Book";"""
SELECT_BOOK_BY_ID = """SELECT "BookName" FROM public."Book" WHERE "BookID" = %s;"""

app = Flask(__name__)
url = "postgresql://postgres:Rikoremot1@localhost:5432/postgres"
connection = psycopg2.connect(url)

@app.get('/api/book_count')
def get_book_count():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(COUNT_BOOK)
            book_count = cursor.fetchone()[0]
    return jsonify({'book_count': book_count})

@app.get('/api/book_name')
def get_book_name():
    book_id = request.args.get('id')
    if not book_id:
        return jsonify({'error': 'Book ID is required'}), 400
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_BOOK_BY_ID, (book_id,))
            result = cursor.fetchone()
            if result:
                book_name = result[0]
                return jsonify({'book_id': book_id, 'book_name': book_name})
            else:
                return jsonify({'error': 'Book not found'}), 404