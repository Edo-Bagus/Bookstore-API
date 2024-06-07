import requests

BASE_URL = 'http://127.0.0.1:5000/api/v1/'

def get_all_books():
    response = requests.get(f'{BASE_URL}/books')
    if response.status_code == 200:
        books = response.json()['books']
        for book in books:
            print(f"\nID: {book['book_id']}, Name: {book['book_name']}, Language: {book['language_id']}, Original Languange: {book['original_language_id']}, Page: {book['pages']}, Price: {book['price']}, Publication Year: {book['publication_year']}")
    else:
        print('Something went wrong')

def get_book_by_author(author):
    response = requests.get(f'{BASE_URL}/books/{author}')
    if response.status_code == 200:
        books = response.json()['books']
        for book in books:
            print(f"\nID: {book['book_id']}, Name: {book['book_name']}, Language: {book['language_id']}, Original Languange: {book['original_language_id']}, Page: {book['pages']}, Price: {book['price']}, Publication Year: {book['publication_year']}")
    else:
        print('Something went wrong')

def delete_book_by_name(book_name):
    response = requests.delete(f'{BASE_URL}/books/{book_name}')
    if response.status_code == 200:
        print('Book deleted successfully')
    else:
        print('Something went wrong')

def add_wishlist():
    customer_name = input("Enter customer name: ")
    book_name = input("Enter book name: ")
    store_name = input("Enter store name: ")

    payload = {
        'customer_name': customer_name,
        'book_name': book_name,
        'store_name': store_name
    }

    response = requests.post(f'{BASE_URL}/add_wishlist', json=payload)
    if response.status_code == 200:
        print('Wishlist added successfully')
    else:
        print('Something went wrong')

def add_review():
    customer_name = input("Enter customer name: ")
    book_name = input("Enter book name: ")
    description = input("Enter description: ")
    rating = input("Enter rating: ")
    
    payload = {
        'customer_name': customer_name,
        'book_name': book_name,
        'description': description,
        'rating': rating
    }
    response = requests.post(f'{BASE_URL}/add_review', json=payload)
    if response.status_code == 200:
        print('Review added successfully')
    else:
        print('Something went wrong')

def update_review():
    customer_name = input("Enter customer name: ")
    book_name = input("Enter book name: ")
    description = input("Enter description: ")
    rating = input("Enter rating: ")
    
    payload = {
        'customer_name': customer_name,
        'book_name': book_name,
        'description': description,
        'rating': rating
    }
    response = requests.put(f'{BASE_URL}/update_review', json=payload)
    if response.status_code == 200:
        print('Review updated successfully')
    else:
        print('Something went wrong')

def main():
    while True:
        print('\nOptions:')
        print("1. Get all books")
        print("2. Get all books by author")
        print("3. Delete book by book name")
        print("4. Add Wishlist")
        print("5. Add Review")
        print("6. Update Review")
        choice = input("Enter choice: ")

        if choice == '1':
            get_all_books()
        elif choice == '2':
            author_choice = input("Enter author: ")
            get_book_by_author(author_choice)
        elif choice == '3':
            book_name = input("Enter book name: ")
            delete_book_by_name(book_name)
        elif choice == '4':
            add_wishlist()
        elif choice == '5':
            add_review()
        elif choice == '6':
            update_review()
        else:
            print("\nInvalid choice, please try again")

if __name__ == '__main__':
    main()