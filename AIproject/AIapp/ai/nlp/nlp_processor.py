import spacy
import re

nlp = spacy.load("en_core_web_sm")

class NLPProcessor:
    def clean(self, text):
        text = text.lower().strip()
        text = text.replace(".", "")
        text = text.replace(",", "")
        text = text.replace("!", "")
        text = text.replace("?", "")
        return text
