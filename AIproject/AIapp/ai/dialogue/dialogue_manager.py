from decimal import Decimal
from AIapp.models import BankAccount, Transaction


class DialogueManager:

    def reply(self, intent, text, session, request):

        if request.user.is_authenticated:
            try:
                account = BankAccount.objects.get(user=request.user)
            except BankAccount.DoesNotExist:
                return "No bank account found for your user."
        else:
            return "User not authenticated."

        if session.get("state") == "transfer_money":

            step = session.get("step")

            if step == "ask_amount":

                if not text.isdigit():
                    return "Please tell me the amount in numbers."

                amount = Decimal(text)
                current_balance = account.balance

                if amount > current_balance:
                    return f"You do not have sufficient funds. Your current balance is {current_balance} pounds."

                session["amount"] = str(amount)
                session["step"] = "ask_account"

                return "To which account would you like to transfer the money? Savings or current?"

            if step == "ask_account":

                if text not in ["savings", "current"]:
                    return "Please specify savings or current account."

                session["account"] = text
                session["step"] = "confirm"

                amount = session.get("amount")

                return (
                    f"You are about to transfer {amount} pounds to {text} account. "
                    f"Do you confirm?"
                )

            if step == "confirm":

                if text in ["yes", "confirm", "sure"]:

                    amount = Decimal(session.get("amount"))
                    account_name = session.get("account")

                    account.balance -= amount
                    account.save()

                    Transaction.objects.create(
                        account=account,
                        amount=amount,
                        target_account=account_name
                    )

                    new_balance = account.balance

                    session["state"] = None
                    session["step"] = None
                    session["amount"] = None
                    session["account"] = None

                    return (
                        f"Transfer of {amount} pounds to {account_name} account completed successfully. "
                        f"Your new balance is {new_balance} pounds."
                    )

                if text in ["no", "cancel"]:
                    session.clear()
                    return "Transfer cancelled."

                return "Please say yes to confirm or no to cancel."

        if intent == "transfer_money":
            session["state"] = "transfer_money"
            session["step"] = "ask_amount"
            return "How much would you like to transfer?"

        if intent == "greeting":
            return "Hello! How can I assist you today?"

        if intent == "check_balance":
            return f"Your current balance is {account.balance} pounds."

        if intent == "recent_transactions":

            transactions = Transaction.objects.filter(
                account=account
            ).order_by("-created_at")[:3]

            if not transactions:
                return "You have no recent transactions."

            response_parts = [
                f"{t.amount} pounds to {t.target_account}"
                for t in transactions
            ]

            return "Your last transactions were: " + ", ".join(response_parts)

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

        return "I’m sorry, I could not clearly understand your request. Please repeat it."