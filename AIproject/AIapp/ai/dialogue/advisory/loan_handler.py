from AIapp.ai.utils.calculator import calculate_monthly_payment


def handle_loan(amount=100000, rate=5, years=20):

    monthly = calculate_monthly_payment(amount, rate, years)

    return f"For a loan of {amount}, monthly payment would be approximately {monthly}."