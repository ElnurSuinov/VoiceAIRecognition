from AIapp.ai.stt.speech_to_text import SpeechToText
from AIapp.ai.nlp.nlp_processor import NLPProcessor
from AIapp.ai.ml.intent_service import get_intent
from AIapp.ai.dialogue.dialogue_manager import DialogueManager
import re


CONFIDENCE_THRESHOLD = 0.6


def run(audio, request):

    stt = SpeechToText()
    nlp = NLPProcessor()
    manager = DialogueManager()

    transcript = stt.transcribe(audio)

    if not transcript:
        return "", "unknown", "I didn't catch that."

    clean_text = nlp.clean(transcript)

    # OTP detection
    if re.fullmatch(r"\d{6}", clean_text):

        intent = "confirm_otp"

        response = manager.handle(
            intent,
            clean_text,
            request
        )

        return transcript, intent, response

    intent, confidence = get_intent(clean_text)

    if confidence < CONFIDENCE_THRESHOLD:

        intent = "unknown"

        response = manager.handle(
            intent,
            clean_text,
            request
        )

        return transcript, intent, response

    response = manager.handle(
        intent,
        clean_text,
        request
    )

    return transcript, intent, response