import numpy as np
import re
import nltk
from sklearn.datasets import load_files
nltk.download('stopwords')
import pickle
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

def frequency(data):
    tokens = [t for t in data.split()]
    
    freq = nltk.FreqDist(tokens)
    for key,val in freq.items():
        print (str(key) + ':' + str(val))

    return freq.items()

def sentiment():
    movie_data = load_files(r'/Users/desarrollo/Desktop/review_polarity/txt_sentoken')
    X, y = movie_data.data, movie_data.target

    documents = []
    stemmer = WordNetLemmatizer()
    for sen in range(0, len(X)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(X[sen]))

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Converting to Lowercase
        document = document.lower()

        # Lemmatization
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)

        documents.append(document)