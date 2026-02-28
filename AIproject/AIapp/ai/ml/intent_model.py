from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class IntentClassifierML:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True
        )
        self.model = LogisticRegression(max_iter=2000)

    def train(self, texts, labels):
        x = self.vectorizer.fit_transform(texts)
        self.model.fit(x, labels)

    def predict(self, text):
        x = self.vectorizer.transform([text])
        probs = self.model.predict_proba(x)[0]

        max_proba = probs.max()
        predicted_intent = self.model.classes_[probs.argmax()]

        return predicted_intent, float(max_proba)