from .stt.speech_to_text import SpeechToText
from .nlp.nlp_processor import NLPProcessor
from .ml.intent_service import get_intent
from .dialogue.dialogue_manager import DialogueManager

CONFIDENCE_THRESHOLD = 0.25

def run(audio_path):
    stt = SpeechToText()
    nlp = NLPProcessor()
    dialogue = DialogueManager()

    text = stt.transcribe(audio_path)
    print(f"[RAW FROM WHISPER] '{text}'")

    if not text or len(text.strip()) < 2:
        return "", "fallback", "Sorry, I didn't catch that. Could you please repeat?"

    clean_text = nlp.clean(text)
    print(f"[AFTER CLEAN] '{clean_text}'")

    intent, confidence = get_intent(clean_text)

    print(f"[ML DEBUG] text='{clean_text}' | intent={intent} | confidence={confidence:.2f}")

    if confidence < CONFIDENCE_THRESHOLD or intent == "unknown":
        return (
            text,
            intent,
            "I'm not confident I understood your request. Could you please rephrase?"
        )

    response = dialogue.reply(intent)

    return text, intent, response
