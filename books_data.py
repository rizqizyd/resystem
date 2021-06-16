import pandas as pd

def data_buku():
    df = pd.read_csv("data_5000.csv", sep='\t', error_bad_lines=False)
    df = df.drop(['Unnamed: 0', 'description', 'site'], axis=1)
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs'}, axis=1)
    df = df.head(21)
    return df