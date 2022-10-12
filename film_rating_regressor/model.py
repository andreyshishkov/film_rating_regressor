from sklearn.svm import SVR
from sklearn.feature_extraction.text import TfidfVectorizer
from text_normalizer import Normalizer
from sklearn.pipeline import Pipeline
import pandas as pd
import pickle


def create_pipeline():
    pipeline = tf_idf_lr = Pipeline([
        ('normalizer', Normalizer()),
        ('tf-idf', TfidfVectorizer(preprocessor=' '.join)),
        ('lr', SVR())
    ])
    return pipeline


if __name__ == '__main__':
    data = pd.read_csv('../data/film_ratings_1.csv', delimiter=';')
    X = data['description']
    y = data['rating']
    model = create_pipeline()
    model.fit(X, y)

    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)
