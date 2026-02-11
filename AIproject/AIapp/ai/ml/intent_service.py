from .training_data import TRAINING_DATA
from .intent_model import IntentClassifierML

texts = [x[0] for x in TRAINING_DATA]
labels = [x[1] for x in TRAINING_DATA]

classifier = IntentClassifierML()
classifier.train(texts, labels)

def get_intent(text):
    return classifier.predict(text)
