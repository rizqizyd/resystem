import pandas as pd

def data_buku():
    df = pd.read_csv("data_soup.csv", sep='\t', error_bad_lines=False)
    df = df[['title', 'author', 'genre', 'image']]

    # ubah string ke list
    df['genre'] = df['genre'].apply(lambda x:x.replace("'", "").replace("[", "").replace("]", ""))
    df['genre'] = df.genre.apply(lambda x: x.split(', '))

    # list genre ke dua
    gen = []
    for genre in df['genre']:
        gen.append(genre[1])

    # list title
    tit = []
    for title in df['title']:
        tit.append(title)

    # hapus genre kedua jika sama dengan title
    x = 0
    for i in df['genre']:
        if i[1] == tit[x]:
            df['genre'][x] = df['genre'][x][0]
        x = x + 1

    # set buku yang memiliki 1 genre menjadi list
    y = 0
    for i in df['genre']:
        if isinstance(i, str):
            df['genre'][y] = i.split("delimiter")
        y = y + 1

    df['genre'] = [', '.join(map(str, l)) for l in df['genre']]
    
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs', 'image':'Cover'}, axis=1)
    df['Cover'] = df['Cover'].apply(lambda x: '<img src="{}" width="100px"/>'.format(x) if x else '')
    df = df.head(21)
    return df