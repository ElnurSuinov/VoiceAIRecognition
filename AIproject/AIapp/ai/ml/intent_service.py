import os
import joblib

from AIapp.ai.ml.intent_model import IntentModel
from AIapp.ai.ml.training_data import TRAINING_DATA


MODEL_PATH = "intent_model.pkl"
VECTORIZER_PATH = "intent_vectorizer.pkl"


def _create_and_train_model():
    model = IntentModel()

    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]

    model.train(texts, labels)

    joblib.dump(model.model, MODEL_PATH)
    joblib.dump(model.vectorizer, VECTORIZER_PATH)

    return model


def _load_existing_model():
    model = IntentModel()
    model.model = joblib.load(MODEL_PATH)
    model.vectorizer = joblib.load(VECTORIZER_PATH)
    return model


def get_model():
    if not os.path.exists(MODEL_PATH):
        return _create_and_train_model()
    return _load_existing_model()


def get_intent(text):
    model = get_model()
    return model.predict(text)