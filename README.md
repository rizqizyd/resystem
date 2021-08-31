# resystem
Sistem Rekomendasi Buku Menggunakan Metode Content Based Filtering

Pada sistem ini terdapat 2 folder yang berfungsi untuk mengatur tampilan (html, css) dari sistem rekomendasi
- folder templates berisi kode untuk mengatur tampilan html
- folder static berisi css dan image untuk memeperindah tampilan website

Pada sistem ini terdapat file-file yang digunakan untuk menjalankan backend dari sistem rekomendasi
- app.py berisi kode utama supaya dapat menjalankan website sistem rekomendasi
- resystem.py berisi kode untuk menjalankan sistem rekomendasi buku berdasarkan judul
- bykeywords.py berisi kode untuk menjalankan sistem rekomendasi buku berdasarkan kata kunci (keywords)
- books_data.py berisi kode untuk menampilkan 20 data buku pertama yang tersedia pada database "data_soup.csv"
- search.py berisi kode untuk mencari data buku yang tersedia pada database "data_soup.csv"

Penjelasan file lain
- data_soup.csv merupakan database yang digunakan untuk menyimpan data-data buku
- Procfile digunakan supaya dapat menjalankan website menggunakan heroku
- requirements.txt digunakan untuk menginstall library yang digunakan ketika website dijalankan pada heroku
