import pandas as pd

# Mengimpor library re dan NLTK
# Mendownload daftar kata yang ada (vocabulary)
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Libraries for Recommendation System
from sklearn.feature_extraction.text import TfidfVectorizer

# Read Data
books = pd.read_csv('data_soup.csv', sep='\t')

# dropping ALL duplicate values
books.drop_duplicates(subset ="title", inplace = True)

# memeriksa daftar kata di stopwords  
indo = stopwords.words('indonesian')  
eng = stopwords.words('english')  
  
# get stopwords from NLTK stopword   
# get stopwords indonesia (758 kata)  
list_stopwords = stopwords.words('indonesian')  
  
# list stopwords bahasa indonesia
list_stopwords = indo  
  
# menambah stopwords bahasa inggris 
list_stopwords.extend(eng)

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words=list_stopwords)
tfidf_matrix = tfidf.fit_transform(books['soup'])

# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

books = books.reset_index()
titles = books['title']
titles = titles.str.lower()
authors = books['author']

# ubah string ke list
books['genre'] = books['genre'].apply(lambda x:x.replace("'", "").replace("[", "").replace("]", ""))
books['genre'] = books.genre.apply(lambda x: x.split(', '))

# list genre ke dua
gen = []
for genre in books['genre']:
    gen.append(genre[1])

# list title
tit = []
for title in books['title']:
    tit.append(title)

# hapus genre kedua jika sama dengan title
x = 0
for i in books['genre']:
    if i[1] == tit[x]:
        books['genre'][x] = books['genre'][x][0]
    x = x + 1

# set buku yang memiliki 1 genre menjadi list
y = 0
for i in books['genre']:
    if isinstance(i, str):
        books['genre'][y] = i.split("delimiter")
    y = y + 1

books['genre'] = [', '.join(map(str, l)) for l in books['genre']]

genres = books['genre']
covers = books['image'].apply(lambda x: '<img src="{}" width="100px"/>'.format(x) if x else '')
indices = pd.Series(books.index, index=titles)

#Construct a reverse map of indices and book titles
indices = pd.Series(books.index, index=titles).drop_duplicates()

# Function that takes in book title as input and outputs most similar books
def get_recommendations(title, jumlah=10, cosine_sim=cosine_sim):
    jumlah = int(jumlah) + 1
    recommendation = pd.DataFrame(columns = ['Judul', 'Penulis', 'Genre', 'Cover'])
    count = 0
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:jumlah]
    book_indices = [i[0] for i in sim_scores]
    
    for i in book_indices:
        recommendation.at[count+1, 'Judul'] = titles.iloc[book_indices[count]].title()
        recommendation.at[count+1, 'Penulis'] = authors.iloc[book_indices[count]].title()
        recommendation.at[count+1, 'Genre'] = genres.iloc[book_indices[count]].title()
        recommendation.at[count+1, 'Cover'] = covers.iloc[book_indices[count]]
        count += 1
    
    return recommendation



