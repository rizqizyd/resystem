import pandas as pd

def data_buku():
    df = pd.read_csv("data_soup(gambar).csv", sep='\t', error_bad_lines=False)
    # df = df.drop(['Unnamed: 0', 'description', 'site', 'title_list', 'author_list', 'genre_list', 'description_list', 'soup'], axis=1)
    df = df[['title', 'author', 'genre', 'image']]
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs', 'image':'Cover'}, axis=1)
    df['Cover'] = df['Cover'].apply(lambda x: '<img src="{}" width="100px"/>'.format(x) if x else '')
    df = df.head(21)
    return df