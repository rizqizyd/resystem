import pandas as pd

def cari_buku(cari):
    df = pd.read_csv("data_soup.csv", sep='\t', error_bad_lines=False)
    df = df[['title', 'author', 'genre', 'image']]
    df = df.rename({'title': 'Judul', 'author': 'Penulis', 'genre': 'Genre','site' :'Situs', 'image': 'Cover'}, axis=1)
    df['Cover'] = df['Cover'].apply(lambda x: '<img src="{}" width="100px"/>'.format(x) if x else '')
    
    # ubah string ke list
    df['Genre'] = df['Genre'].apply(lambda x:x.replace("'", "").replace("[", "").replace("]", ""))
    df['Genre'] = df.Genre.apply(lambda x: x.split(', '))

    # list Genre ke dua
    gen = []
    for Genre in df['Genre']:
        gen.append(Genre[1])

    # list title
    tit = []
    for title in df['Judul']:
        tit.append(title)

    # hapus Genre kedua jika sama dengan title
    x = 0
    for i in df['Genre']:
        if i[1] == tit[x]:
            df['Genre'][x] = df['Genre'][x][0]
        x = x + 1

    # set buku yang memiliki 1 Genre menjadi list
    y = 0
    for i in df['Genre']:
        if isinstance(i, str):
            df['Genre'][y] = i.split("delimiter")
        y = y + 1

    df['Genre'] = [', '.join(map(str, l)) for l in df['Genre']]

    df = df.apply(lambda x: x.astype(str).str.lower())
    filt = df[(df['Judul'].str.contains(cari)) | (df['Penulis'].str.contains(cari)) | (df['Genre'].str.contains(cari))]
    hasil = filt.copy()

    hasil[['Judul', 'Penulis', 'Genre']] = hasil[['Judul', 'Penulis', 'Genre']].apply(lambda x: x.astype(str).str.title())
    return hasil