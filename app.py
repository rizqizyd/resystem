from flask import Flask, render_template, request

import books_data as bd
import search as src

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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