from flask import Blueprint, jsonify, request
from services.Service import add_wishlist_service

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/api/v1/add_wishlist', methods=['POST'])
def add_wishlist():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Customer name, Book name, and Store name is required'})
    
    customer_name = data.get('customer_name')
    book_name = data.get('book_name')
    store_name = data.get('store_name')
    success = add_wishlist_service(customer_name, book_name, store_name)
    if success:
        return jsonify({'message': 'Wishlist added successfully'}), 200
    else:
        return jsonify({'message': 'Error adding wishlist book'}), 500