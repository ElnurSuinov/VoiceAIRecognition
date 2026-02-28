from .stt.speech_to_text import SpeechToText
from .nlp.nlp_processor import NLPProcessor
from .ml.intent_service import get_intent
from .dialogue.dialogue_manager import DialogueManager

CONFIDENCE_THRESHOLD = 0.40


def rule_based_fallback(text):
    if "transfer" in text or "send money" in text:
        return "transfer_money"
    if "balance" in text:
        return "check_balance"
    if "transaction" in text or "payment" in text:
        return "recent_transactions"
    return None


def run(audio_path, request):

    stt = SpeechToText()
    nlp = NLPProcessor()
    dialogue = DialogueManager()

    text = stt.transcribe(audio_path)

    if not text or len(text.strip()) < 1:
        return "", "fallback", "Sorry, I didn't catch that."

    clean_text = nlp.clean(text)

    # Если идёт активный диалог
    if request.session.get("state"):
        response = dialogue.reply(None, clean_text, request.session, request)
        return text, "in_progress", response

    # ML предсказание
    intent, confidence = get_intent(clean_text)

    print(f"[ML DEBUG] text='{clean_text}' | intent={intent} | confidence={confidence:.2f}")

    # Если уверенность низкая — применяем rule fallback
    if confidence < CONFIDENCE_THRESHOLD:
        rule_intent = rule_based_fallback(clean_text)
        if rule_intent:
            intent = rule_intent
        else:
            return text, intent, "Could you please rephrase your request?"

    response = dialogue.reply(intent, clean_text, request.session, request)

    return text, intent, response