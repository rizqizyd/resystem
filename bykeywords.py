# Mengimpor library
import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')
from nltk.tokenize import word_tokenize
# import Sastrawi package  
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  
# import swifter   
# Libraries for Recommendation System
from sklearn.feature_extraction.text import TfidfVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

def get_recommendations(judul, jumlah):
    # Tokenize
    # Creates Series
    judul = pd.Series(judul)  

    judul = judul.apply(lambda x: x.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"").replace("http://", " ").replace("https://", " "))  
    judul = judul.apply(lambda x: x.encode('ascii', 'replace').decode('ascii'))  
    judul = judul.apply(lambda x: ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", x).split()))  
    judul = judul.apply(lambda x: re.sub(r"\d+", "", x))  
    judul = judul.apply(lambda x: x.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+—"})) 
    judul = judul.apply(lambda x: x.strip())  
    judul = judul.apply(lambda x: re.sub('\s+',' ', x))  
    judul = judul.apply(lambda x: re.sub(r"\b[a-zA-Z]\b", "", x)) 

    # create series form a list
    judul = pd.Series(judul)
    print(judul)

    judul = judul.apply(lambda x: word_tokenize(x)) 
    judul

    # Filtering
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

    # hapus stopword pada list token  
    def stopwords_removal(words):  
        return [word for word in words if word not in list_stopwords]

    judul = judul.apply(stopwords_removal)

    # Stemming    
    # create stemmer  
    # factory = StemmerFactory()  
    # stemmer = factory.create_stemmer()  

    # term_dict = {}  
    
    # for document in judul:  
    #     for term in document:  
    #         if term not in term_dict:  
    #             term_dict[term] = ' '  

    # # stemmed
    # for term in term_dict:  
    #     term_dict[term] = stemmer.stem(term)  
    #     print(term,":" ,term_dict[term])  

    # # apply stemmed term to dataframe  
    # def get_stemmed_term(document):  
    #     return [term_dict[term] for term in document]  
    
    # judul = judul.swifter.apply(get_stemmed_term)

    # Ambil keywords
    judul = judul.to_string()
    judul = judul[6:-1]
    judul = re.sub(r'[^\w\s]', '', judul)
    
    # Read Data
    books = pd.read_csv('data_soup.csv', sep='\t')
    gnr = "['keywords', {judul}]"
    data = [{'Unnamed: 0': 5143, 'Unnamed: 0.1':5154, 'title': judul, 'author': judul, 'genre': gnr, 'description': judul, 'image': judul, 'site': judul, 'title_list': judul, 'author_list': judul, 'genre_list': judul, 'description_list': judul, 'soup': judul}]

    # Creates DataFrame
    new = pd.DataFrame(data)  
    frames = [books, new]
    result = pd.concat(frames)
    books = result.copy()

    # memeriksa daftar kata di stopwords  
    indo = stopwords.words('indonesian')  
    eng = stopwords.words('english')  
    
    # get stopwords from NLTK stopword  
    list_stopwords = stopwords.words('indonesian')  
    # list stopwords bahasa indonesia (758 kata)
    list_stopwords = indo  
    # menambah stopwords bahasa inggris 
    list_stopwords.extend(eng)

    books['soup'] = books['soup'].fillna('')

    # TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words=list_stopwords)
    tfidf_matrix = tfidf.fit_transform(books['soup'])

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

    # Function that takes in book title as input and outputs most similar books
    jumlah = int(jumlah) + 1
    recommendation = pd.DataFrame(columns = ['Judul', 'Penulis', 'Genre', 'Cover'])
    count = 0
        
    idx = indices[judul]
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