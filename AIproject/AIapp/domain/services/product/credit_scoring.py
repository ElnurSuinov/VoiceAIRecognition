class CreditScoring:

    def evaluate(self, user, income, existing_loans):

        score = 50

        if income > 3000:
            score += 20

        if income > 7000:
            score += 30

        if existing_loans > income * 0.5:
            score -= 30

        return max(0, min(score, 100))