from AIapp.ai.ml.intent_service import get_intent


def classify(text):

    intent, confidence = get_intent(text)

    return intent