from repository.BookRepo import get_all_books, get_books_by_author, delete_books_by_name
from repository.WishlistRepo import add_wishlist
from repository.ReviewsRepo import add_review

def get_all_books_service():
    return get_all_books()

def get_books_by_author_service(author):
    return get_books_by_author(author)

def delete_books_by_name_service(name):
    return delete_books_by_name(name)

def add_wishlist_service(customer_name, book_name, store_name):
    return add_wishlist(customer_name, book_name, store_name)

def add_review_service(customer_name, book_name, description, rating):
    return add_review(customer_name, book_name, description, rating)