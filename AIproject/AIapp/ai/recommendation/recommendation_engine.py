class RecommendationEngine:

    def recommend(self, intent):

        if intent == "advisory_loan":
            return "We recommend our mortgage plan with 4.5% interest."

        return "We offer several financial products tailored to your needs."