# Bookstore-API

Good Reading Bookstore adalah sebuah toko buku yang ingin meluaskan usahanya ke bidang online. Dari sistem bisnis GRB, didapatkan ERD:
![Good Reading Bookstore ERD](https://github.com/Edo-Bagus/Bookstore-API/blob/main/assets/TBD.png)

Penggunaan RESTful API untuk database Good Reading Store memberikan manfaat besar dalam mengelola informasi seperti daftar buku, stok, dan transaksi secara efisien. Dengan API, pengembang dapat mengintegrasikan data dengan berbagai aplikasi dan platform lainnya, meningkatkan keterjangkauan data, serta mempercepat pengembangan dan iterasi produk. API yang dikembangkan menggunakan framework Flask menggunakan Bahasa pemrograman Python. Untuk saat ini, dan untuk simplisitas, API yang dikembangkan baru mengimplementasi 6 logika bisnis dengan 6 endpoint:

## API Endpoints

1. **GET /api/v1/books**:
   - Untuk mendapatkan data semua buku dari GRB

2. **GET /api/v1/books/<author>**:
   - Untuk mendapatkan data semua buku dari author tertentu

3. **DELETE /api/v1/books/<book_name>**:
   - Menghapus data suatu buku dari nama buku

4. **POST /api/v1/add_wishlist**:
   - Menambah wishlist dari satu customer

5. **POST /api/v1/add_review**:
   - Menambah review buku dari satu customer

6. **PUT /api/v1/update_review**:
   - Mengubah review buku dari satu customer

## Installation
1. Clone  repository:
    ```bash
    git clone https://github.com/Edo-Bagus/Bookstore-API.git
    cd Bookstore-API
    ```
2. Vuat virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Running the API
Untuk menjalakan API, jalankan Flask app terlebih dahulu:
```bash
flask run
 ```
Lalu akan mendapat URL lokal (seperti `http://127.0.0.1:5000/). URL tersebut dapat digunakan untuk menguji endpoit menggunakan Postman.
API juga dapat diuji dengan menjalankan aplikasi terminal yang ada dengan cara:
```bash
python .\terminal-app.py
```
