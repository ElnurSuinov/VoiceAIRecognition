import re
import spacy

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


WORD_TO_NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "hundred": 100, "thousand": 1000,
    "a hundred": 100, "a thousand": 1000,
    "two hundred": 200, "three hundred": 300,
    "four hundred": 400, "five hundred": 500,
}


def extract_amount(text: str):
    nlp = _get_nlp()
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ in ("MONEY", "CARDINAL"):
            raw = ent.text.lower().replace(",", "").strip()

            if re.fullmatch(r"\d{6}", raw):
                continue

            try:
                amount = int(float(raw))
                if 1 <= amount <= 100000:
                    return amount
            except ValueError:
                pass

            if raw in WORD_TO_NUM:
                return WORD_TO_NUM[raw]

    for match in re.finditer(r"\b(\d+)\b", text):
        amount = int(match.group())
        if len(match.group()) == 6:
            continue
        if 1 <= amount <= 100000:
            return amount

    return None


def extract_account_number(text: str):
    match = re.search(r"\b\d{8,20}\b", text)
    if match:
        return match.group()
    return None