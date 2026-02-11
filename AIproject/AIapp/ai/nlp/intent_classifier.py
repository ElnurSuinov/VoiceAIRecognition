class IntentClassifier:
    def get_intent(self, text):
        if "hello" in text:
            return "greeting"
        elif "balance" in text:
            return "balance"
        elif "bill" in text:
            return  "billing"
        elif "bye" in text:
            return "goodbye"
        return "unknown"