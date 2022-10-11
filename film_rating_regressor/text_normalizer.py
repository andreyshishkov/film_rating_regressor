from sklearn.base import BaseEstimator, TransformerMixin
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer


class Normalizer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.__punct = '!"#$%&()*\+,-\./:;<=>?@\[\]^_`{|}~„“«»†*\—/\-‘’'
        self.__stop_words = stopwords.words('russian')
        self.__morph = MorphAnalyzer()

    def fit(self, X, y=None):
        return self

    def transform(self, descriptions):
        for document in descriptions:
            yield self.normalize(document)

    def normalize(self, text):
        text = text.replace('\xa0', ' ')

        tokens = word_tokenize(text)
        tokens = [w.strip(self.__punct) for w in tokens]
        tokens = [word.lower() for word in tokens if word != '']
        tokens = [word for word in tokens if word not in self.__stop_words]
        tokens = [self.__morph.parse(word)[0].normal_form for word in tokens]

        return tokens
