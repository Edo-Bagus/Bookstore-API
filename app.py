from flask import Flask
from routes.BookRoute import books_bp
from routes.WishlistRoute import wishlist_bp

app = Flask(__name__)
app.register_blueprint(books_bp)
app.register_blueprint(wishlist_bp)