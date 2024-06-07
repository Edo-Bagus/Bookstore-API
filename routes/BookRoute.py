from flask import Blueprint, jsonify, request
from services.Service import get_all_books_service, get_books_by_author_service, delete_books_by_name_service

books_bp = Blueprint('books', __name__)

@books_bp.route('/api/v1/books', methods=['GET'])
def get_books():
    books, error_msg = get_all_books_service()

    if books:
        books_list = [{
            'book_id': book.book_id,
            'book_name': book.book_name,
            'publication_year': book.publication_year,
            'pages': book.pages,
            'price': book.price,
            'language_id': book.language_id,
            'original_language_id': book.original_language_id,
            'publisher_id': book.publisher_id,
        } for book in books]
        return jsonify({'books': books_list}), 200
    else: 
        return jsonify({'message': 'Failed to get book', 'error': error_msg}), 404

@books_bp.route('/api/v1/books/<author>', methods=['GET'])
def get_books_by_author(author):
    
    books, error_msg = get_books_by_author_service(author)
    if books:
        books_list = [{
            'book_id': book.book_id,
            'book_name': book.book_name,
            'publication_year': book.publication_year,
            'pages': book.pages,
            'price': book.price,
            'language_id': book.language_id,
            'original_language_id': book.original_language_id,
            'publisher_id': book.publisher_id,
        } for book in books]
        return jsonify({'books': books_list}), 200
    else:
        return jsonify({'message': 'Failed to get book', 'error': error_msg}), 404
    
@books_bp.route('/api/v1/books/<book_name>', methods=['DELETE'])
def delete_book_by_name(book_name):  
    success, error_msg = delete_books_by_name_service(book_name)
    if success:
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Error deleting book', 'error': error_msg}), 500