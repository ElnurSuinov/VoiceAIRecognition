import os
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer


BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "intent_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")


class IntentModel:

    def __init__(self):
        self.model = None
        self.vectorizer = None

    def train(self, texts, labels):

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=2000
        )

        x = self.vectorizer.fit_transform(texts)

        self.model = LogisticRegression(
            max_iter=1000
        )

        self.model.fit(x, labels)

        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.vectorizer, VECTORIZER_PATH)

    def load(self):

        if not os.path.exists(MODEL_PATH):
            raise Exception("Model not trained")

        self.model = joblib.load(MODEL_PATH)
        self.vectorizer = joblib.load(VECTORIZER_PATH)

    def predict(self, text):

        x = self.vectorizer.transform([text])

        prediction = self.model.predict(x)[0]
        probabilities = self.model.predict_proba(x)[0]

        confidence = max(probabilities)

        return prediction, confidence