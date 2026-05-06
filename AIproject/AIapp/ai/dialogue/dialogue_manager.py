from AIapp.application.transfer_service import TransferService
from AIapp.application.balance_service import BalanceService
from AIapp.application.transaction_service import TransactionService
from AIapp.ai.recommendation.recommendation_engine import RecommendationEngine
from AIapp.ai.utils.entity_extractor import extract_amount
from AIapp.ai.llm.llm_service import LLMService
from AIapp.ai.dialogue.advisory.deposit_handler import handle_deposit
from AIapp.ai.dialogue.advisory.loan_handler import handle_loan


class DialogueManager:

    def __init__(self):

        self.transfer_service = TransferService()
        self.balance_service = BalanceService()
        self.transaction_service = TransactionService()
        self.recommendation_engine = RecommendationEngine()
        self.llm = LLMService()

    def handle(self, intent, text, request):

        user = request.user

        # -------------------------------
        # GREETING
        # -------------------------------

        if intent == "greeting":

            return (
                f"Hello {user.first_name or user.username}! I am your AI banking assistant. "
                "I can help you with balances, transfers, loans, "
                "deposits, cards and financial advice."
            )

        # -------------------------------
        # CHECK BALANCE
        # -------------------------------

        if intent == "check_balance":

            balance = self.balance_service.get_balance(user)

            return f"Your current balance is {balance} pounds."

        # -------------------------------
        # MONEY TRANSFER
        # -------------------------------

        if intent == "transfer_money":

            amount = extract_amount(text)

            if not amount:

                return "Please specify the transfer amount."

            result = self.transfer_service.execute(
                user,
                amount,
                "default"
            )

            if isinstance(result, dict):

                request.session["pending_transaction"] = result.get(
                    "transaction_id"
                )

                return result["message"]

            return result

        # -------------------------------
        # CONFIRM OTP
        # -------------------------------

        if intent == "confirm_otp":

            transaction_id = request.session.get("pending_transaction")

            if not transaction_id:

                return "There is no pending transaction to confirm."

            result = self.transfer_service.confirm_2fa(
                transaction_id,
                text
            )

            request.session["pending_transaction"] = None

            return result

        # -------------------------------
        # TRANSACTION HISTORY
        # -------------------------------

        if intent == "recent_transactions":

            transactions = self.transaction_service.get_recent_transactions(user)

            if not transactions:

                return "You have no recent transactions."

            result = []

            for t in transactions:

                result.append(f"{t.amount} pounds")

            return "Your recent transactions: " + ", ".join(result)

        # -------------------------------
        # LOANS
        # -------------------------------

        if intent == "loan_info":

            return (
                "We offer several loan options including "
                "personal loans, auto loans and mortgages."
            )

        # -------------------------------
        # DEPOSITS
        # -------------------------------

        if intent == "deposit_info":

            return (
                "We offer fixed-term deposits and flexible "
                "savings accounts with competitive interest rates."
            )

        # -------------------------------
        # CARDS
        # -------------------------------

        if intent == "card_info":

            return (
                "Our bank offers debit and credit cards "
                "with cashback, travel rewards and mobile payments."
            )

        # -------------------------------
        # INSURANCE
        # -------------------------------

        if intent == "insurance_info":

            return (
                "We provide insurance products including "
                "life insurance, health insurance and property insurance."
            )

        # -------------------------------
        # INVESTMENTS
        # -------------------------------

        if intent == "investment_info":

            return (
                "You can invest through our bank using mutual funds, "
                "government bonds or managed portfolios."
            )

        # -------------------------------
        # INTERNET BANKING
        # -------------------------------

        if intent == "internet_banking":

            return (
                "You can access internet banking through "
                "our website or mobile banking application."
            )

        # -------------------------------
        # LOAN RECOMMENDATION
        # -------------------------------

        if intent == "advisory_loan":

            return self.recommendation_engine.recommend(intent)

        # -------------------------------
        # LLM FALLBACK
        # -------------------------------

        if intent is None or intent == "unknown":
            return self.llm.generate(text)

        return self.llm.generate(text)