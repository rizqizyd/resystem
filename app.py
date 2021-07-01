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
        
    df = pd.read_csv("data_soup(fix).csv", sep='\t', error_bad_lines=False)
    x = df.title.values
    search_book = list(map(lambda x: x.lower(), x))
    gagal = 'Buku tidak tersedia atau penulisan judul buku tidak sesuai, silahkan cari ketersediaan buku pada halaman'
    if book not in search_book:
        return render_template("rekomendasi.html", salah=gagal)

    rekomendasi = rec.get_recommendations(book, jumlah)
    # convert your links to html tags 
    def path_to_image_html(path):
        return '<img src="'+ path + '" width="5px" >'

    image_cols = rekomendasi['Cover']  #<- define which columns will be used to convert to html

    # Create the dictionariy to be passed as formatters
    format_dict = {}
    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html

    return render_template("rekomendasi.html", tables=[rekomendasi.to_html(classes='data', escape=False ,formatters=format_dict)], titles=['Title'], buku_dicari=book)

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'GET':
        df = bd.data_buku()
        # convert your links to html tags 
        def path_to_image_html(path):
            return '<img src="'+ path + '" width="5px" >'

        image_cols = df['Cover']  #<- define which columns will be used to convert to html

        # Create the dictionariy to be passed as formatters
        format_dict = {}
        for image_col in image_cols:
            format_dict[image_col] = path_to_image_html
        return render_template('data.html', tables=[df.to_html(classes='data', escape=False ,formatters=format_dict)], titles=['Title'])
    elif request.method == 'POST':
        cari = request.form['cari']
        if cari == '':
            df = bd.data_buku()
            # convert your links to html tags 
            def path_to_image_html(path):
                return '<img src="'+ path + '" width="5px" >'

            image_cols = df['Cover']  #<- define which columns will be used to convert to html

            # Create the dictionariy to be passed as formatters
            format_dict = {}
            for image_col in image_cols:
                format_dict[image_col] = path_to_image_html
            return render_template('data.html', tables=[df.to_html(classes='data', escape=False ,formatters=format_dict)], titles=['Title'])
            
        cari = cari.lower()
        pencarian = src.cari_buku(cari)
        # convert your links to html tags 
        def path_to_image_html(path):
            return '<img src="'+ path + '" width="5px" >'

        image_cols = pencarian['Cover']  #<- define which columns will be used to convert to html

        # Create the dictionariy to be passed as formatters
        format_dict = {}
        for image_col in image_cols:
            format_dict[image_col] = path_to_image_html
        return render_template('data.html', tables=[pencarian.to_html(classes='data', escape=False ,formatters=format_dict)], titles=['Title'])

if __name__ == "__main__":
    app.run()