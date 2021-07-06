import pandas as pd

# Mengimpor library re dan NLTK
import nltk
 
# Mendownload daftar kata yang ada (vocabulary)
nltk.download('stopwords')
from nltk.corpus import stopwords

# Libraries for Recommendation System
from sklearn.feature_extraction.text import TfidfVectorizer

import warnings; warnings.simplefilter('ignore')

# Read Data
books = pd.read_csv('data_soup.csv', sep='\t')

# Memeriksa daftar kata di stopwords bahasa Indonesia
indo = stopwords.words('indonesian')

# TF-IDF Vectorizer
#Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words=indo)
#Replace NaN with an empty string
books['soup'] = books['soup'].fillna('')
#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(books['soup'])
#Output the shape of tfidf_matrix
tfidf_matrix.shape

# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

cosine_sim.shape

books = books.reset_index()
titles = books['title']
titles = titles.str.lower()
authors = books['author']
genres = books['genre']
covers = books['image'].apply(lambda x: '<img src="{}" width="100px"/>'.format(x) if x else '')
# for genre in genres_list.values():
#     genres = genres.title()
# genres = ' '.join(map(str,books['genre']))
# print(genres.dtype)
indices = pd.Series(books.index, index=titles)

#Construct a reverse map of indices and movie titles
indices = pd.Series(books.index, index=titles).drop_duplicates()

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, jumlah=10, cosine_sim=cosine_sim):
    # title = title.lower()
    jumlah = int(jumlah) + 1

    recommendation = pd.DataFrame(columns = ['Judul', 'Penulis', 'Genre', 'Cover'])
    count = 0
    
    # Get the index of the movie that matches the title
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:jumlah]
    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    
    for i in movie_indices:
        # recommendation.at[count, 'Book Idx'] = movie_indices[count]
        recommendation.at[count+1, 'Judul'] = titles.iloc[movie_indices[count]].title()
        recommendation.at[count+1, 'Penulis'] = authors.iloc[movie_indices[count]].title()
        recommendation.at[count+1, 'Genre'] = genres.iloc[movie_indices[count]].title()
        recommendation.at[count+1, 'Cover'] = covers.iloc[movie_indices[count]]
        # gen = genres.iloc[movie_indices[count]]
        # genres2 = ' '.join(map(str, gen))
        # recommendation.at[count+1, 'Genre'] = gen.title()
        # recommendation.at[count, 'Score'] = sim_scores[count][1]
        count += 1
    # Return the top 10 most similar movies
    return recommendation



