import pandas as pd

def cari_buku(cari):
    df = pd.read_csv("data_5000.csv", sep='\t', error_bad_lines=False)
    df = df.drop(['Unnamed: 0', 'description', 'site'], axis=1)
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs'}, axis=1)

    df = df.apply(lambda x: x.astype(str).str.lower())
    # df["Judul"] = df["Judul"].str.lower()
    # filt = df[df['Judul'].str.contains(cari)]
    filt = df[(df['Judul'].str.contains(cari)) | (df['Penulis'].str.contains(cari)) | (df['Genre'].str.contains(cari))]
    # filter_penulis = df[df['Judul'].str.contains(cari)]
    # filt = (df['Judul'] == cari)
    # hasil = df[filt].copy()
    hasil = filt.copy()

    hasil = hasil.apply(lambda x: x.astype(str).str.title())
    # hasil["Judul"] = hasil["Judul"].str.title()
    return hasil