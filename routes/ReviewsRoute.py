from flask import Blueprint, jsonify, request
from services.Service import add_review_service

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/api/v1/add_review', methods=['POST'])
def add_review():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Customer name, Book name, Description, and rating is required'})
    
    customer_name = data.get('customer_name')
    book_name = data.get('book_name')
    description = data.get('description')
    rating = data.get('rating')
    success, error_msg = add_review_service(customer_name, book_name, description, rating)
    if success:
        return jsonify({'message': 'Review added successfully'}), 200
    else:
        return jsonify({'message': 'Error adding review book', 'error': error_msg}), 500
