from AIapp.ai.llm.llm_service import LLMService
from AIapp.domain.services.product.product_service import ProductService


class RecommendationEngine:

    def __init__(self):
        self.llm = LLMService()
        self.products = ProductService()

    def recommend(self, intent):

        if intent == "advisory_loan":
            loans = self.products.get_loans()
            products_text = self._format_loans(loans)
            prompt = f"""You are a professional banking advisor.
A client is asking for loan advice.

Available loan products at our bank:
{products_text}

Give a clear, friendly recommendation. Be specific about rates and terms.
Keep the answer under 3 sentences."""

        elif intent == "advisory_deposit":
            deposits = self.products.get_deposits()
            products_text = self._format_deposits(deposits)
            prompt = f"""You are a professional banking advisor.
A client wants to open a deposit.

Available deposit products at our bank:
{products_text}

Give a clear, friendly recommendation. Be specific about rates and terms.
Keep the answer under 3 sentences."""

        elif intent == "card_info":
            cards = self.products.get_cards()
            products_text = self._format_cards(cards)
            prompt = f"""You are a professional banking advisor.
A client is asking about bank cards.

Available cards at our bank:
{products_text}

Give a clear, friendly recommendation.
Keep the answer under 3 sentences."""

        else:
            return self.llm.generate(intent)

        return self.llm.generate_with_prompt(prompt)

    def _format_loans(self, loans):
        if not loans:
            return "No loan products available."
        lines = []
        for loan in loans:
            lines.append(
                f"- {loan.name}: {loan.interest_rate}% rate, "
                f"{loan.term_months} months, "
                f"min amount {loan.minimum_amount}"
            )
        return "\n".join(lines)

    def _format_deposits(self, deposits):
        if not deposits:
            return "No deposit products available."
        lines = []
        for d in deposits:
            lines.append(
                f"- {d.name}: {d.interest_rate}% rate, "
                f"{d.term_months} months, "
                f"min amount {d.minimum_amount}"
            )
        return "\n".join(lines)

    def _format_cards(self, cards):
        if not cards:
            return "No card products available."
        lines = []
        for card in cards:
            lines.append(
                f"- {card.name}: {card.cashback_percent}% cashback, "
                f"annual fee {card.annual_fee}"
            )
        return "\n".join(lines)