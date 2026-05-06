import re
import spacy

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


class NLPProcessor:

    def clean(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def lemmatize(self, text: str) -> str:
        nlp = _get_nlp()
        doc = nlp(text)
        tokens = [
            token.lemma_
            for token in doc
            if not token.is_stop and not token.is_punct
        ]
        return " ".join(tokens)