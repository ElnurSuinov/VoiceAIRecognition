class DialogueManager:
    def reply(self, intent):

        if intent == "greeting":
            return "Hello! How can I assist you today?"

        if intent == "check_balance":
            return "Your current balance is five hundred pounds."

        if intent == "recent_transactions":
            return "Your last transactions were groceries and online shopping."

        if intent == "card_block":
            return "Your card has been blocked for security reasons."

        if intent == "lost_card":
            return "I have blocked your card. A new one will be issued."

        if intent == "pin_reset":
            return "A PIN reset request has been submitted."

        if intent == "branch_hours":
            return "Our branches are open from 9 AM to 5 PM."

        if intent == "contact_support":
            return "I am transferring you to a customer support agent."

        if intent == "goodbye":
            return "Thank you for calling. Have a nice day."

        return (
            "I’m sorry, I could not clearly understand your request. "
            "Please repeat it."
        )
