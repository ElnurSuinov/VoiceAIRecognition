from AIapp.ai.stt.speech_to_text import SpeechToText
from AIapp.ai.nlp.nlp_processor import NLPProcessor
from AIapp.ai.ml.intent_service import get_intent
from AIapp.ai.dialogue.dialogue_manager import DialogueManager
import re


CONFIDENCE_THRESHOLD = 0.20


def run(audio, request):

    stt = SpeechToText()
    nlp = NLPProcessor()
    manager = DialogueManager()

    transcript = stt.transcribe(audio)

    if not transcript:
        return "", "unknown", "I didn't catch that."

    clean_text = nlp.clean(transcript)

    # OTP detection
    otp_match = re.search(r"\b\d{6}\b", clean_text)
    if otp_match:
        intent = "confirm_otp"
        otp_code = otp_match.group()
        response = manager.handle(intent, otp_code, request)
        return transcript, intent, response

    lemmatized = nlp.lemmatize(clean_text)

    intent, confidence = get_intent(lemmatized)

    if confidence < CONFIDENCE_THRESHOLD:
        return transcript, intent, manager.handle(None, clean_text, request)

    response = manager.handle(
        intent,
        clean_text,
        request
    )

    return transcript, intent, response