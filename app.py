from flask import Flask, render_template, request
import pandas as pd

import resystem as rec
import books_data as bd
import search as src

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/rekomendasi', methods=['GET'])
def rekomendasi():
    return render_template('rekomendasi.html')

@app.route('/rekomendasi', methods=['POST'])
def recommendation():
    book = request.form['book']
    jumlah = request.form['jumlah']
    book = book.lower()
    peringatan = 'Silahkan isi judul buku terlebih dahulu.'
    if book == '':
        return render_template("rekomendasi.html", warning=peringatan) 
    elif jumlah == '':
        jumlah = 10
        
    df = pd.read_csv("data_5000.csv", sep='\t', error_bad_lines=False)
    x = df.title.values
    search_book = list(map(lambda x: x.lower(), x))
    gagal = 'Buku tidak tersedia atau penulisan judul buku tidak sesuai, silahkan cari ketersediaan buku pada halaman'
    if book not in search_book:
        return render_template("rekomendasi.html", salah=gagal)

    rekomendasi = rec.get_recommendations(book, jumlah)

    return render_template("rekomendasi.html", tables=[rekomendasi.to_html(classes='data')], titles=['Title'], buku_dicari=book)

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        df = bd.data_buku()
        return render_template('data.html', tables=[df.to_html(classes='data')], titles=['Title'])
    elif request.method == 'POST':
        cari = request.form['cari']
        if cari == '':
            df = bd.data_buku()
            return render_template('data.html', tables=[df.to_html(classes='data')], titles=['Title'])
        cari = cari.lower()
        pencarian = src.cari_buku(cari)
        return render_template('data.html', tables=[pencarian.to_html(classes='data')], titles=['Title'])

if __name__ == "__main__":
    app.run()