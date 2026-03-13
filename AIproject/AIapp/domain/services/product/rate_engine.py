class RateEngine:

    def calculate_deposit_profit(self, amount, rate, months):

        yearly_profit = amount * (rate / 100)

        monthly_profit = yearly_profit / 12

        return monthly_profit * months

    def calculate_loan_payment(self, amount, rate, months):

        monthly_rate = rate / 100 / 12

        payment = (
            amount * monthly_rate
        ) / (1 - (1 + monthly_rate) ** (-months))

        return payment