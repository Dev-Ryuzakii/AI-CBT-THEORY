from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import joblib

def extract_features(corpus, vectorizer=None):
    if vectorizer is None:
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(corpus)
    else:
        X = vectorizer.transform(corpus)
    return X, vectorizer

def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

def save_model(model, vectorizer, model_path, vectorizer_path):
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
