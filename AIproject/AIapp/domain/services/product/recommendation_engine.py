from AIapp.models import DepositProduct, LoanProduct, CardProduct


class RecommendationEngine:

    def recommend_deposit(self, amount):

        return (
            DepositProduct.objects
            .filter(minimum_amount__lte=amount)
            .order_by("-interest_rate")
            .first()
        )

    def recommend_loan(self, income):

        return (
            LoanProduct.objects
            .filter(minimum_amount__lte=income)
            .order_by("interest_rate")
            .first()
        )

    def recommend_card(self):

        return (
            CardProduct.objects
            .order_by("-cashback_percent")
            .first()
        )