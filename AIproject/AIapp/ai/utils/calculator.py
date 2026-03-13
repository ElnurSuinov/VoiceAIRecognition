def calculate_monthly_payment(amount, annual_rate, years):

    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    payment = amount * (monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)

    return round(payment, 2)