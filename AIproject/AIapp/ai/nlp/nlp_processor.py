import re


class NLPProcessor:

    def clean(self, text):

        text = text.lower()

        text = re.sub(r"[^\w\s]", "", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()