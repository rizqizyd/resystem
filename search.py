import pandas as pd

def cari_buku(cari):
    df = pd.read_csv("data_soup(fix).csv", sep='\t', error_bad_lines=False)
    # df = df.drop(['Unnamed: 0', 'description', 'site', 'title_list', 'author_list', 'genre_list', 'description_list', 'soup'], axis=1)
    df = df[['title', 'author', 'genre', 'image']]
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs', 'image': 'Cover'}, axis=1)
    df['Cover'] = df['Cover'].apply(lambda x: '<img src="{}" width="100px"/>'.format(x) if x else '')

    df = df.apply(lambda x: x.astype(str).str.lower())
    # df["Judul"] = df["Judul"].str.lower()
    # filt = df[df['Judul'].str.contains(cari)]
    filt = df[(df['Judul'].str.contains(cari)) | (df['Penulis'].str.contains(cari)) | (df['Genre'].str.contains(cari))]
    # filter_penulis = df[df['Judul'].str.contains(cari)]
    # filt = (df['Judul'] == cari)
    # hasil = df[filt].copy()
    hasil = filt.copy()

    hasil[['Judul', 'Penulis', 'Genre']] = hasil[['Judul', 'Penulis', 'Genre']].apply(lambda x: x.astype(str).str.title())
    # hasil["Judul"] = hasil["Judul"].str.title()
    return hasil