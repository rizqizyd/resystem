import pandas as pd

def data_buku():
    df = pd.read_csv("data_soup.csv", sep='\t', error_bad_lines=False)
    df = df.drop(['Unnamed: 0', 'description', 'site', 'title_list', 'author_list', 'genre_list', 'description_list', 'soup'], axis=1)
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs'}, axis=1)
    df = df.head(21)
    return df