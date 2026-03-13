from celery import shared_task

from AIapp.models import Transaction
from AIapp.risk.risk_engine import RiskEngine


@shared_task
def send_otp_task(user_id, code):

    print(f"Sending OTP {code} to user {user_id}")

    return True


@shared_task
def fraud_check_task(transaction_id):

    print(f"Running fraud check for transaction {transaction_id}")

    try:
        transaction = Transaction.objects.get(id=transaction_id)

        engine = RiskEngine()

        risk_score = engine.evaluate(
            transaction.account.user,
            transaction.amount,
            None
        )

        transaction.risk_score = risk_score
        transaction.save(update_fields=["risk_score"])

        print(f"Transaction {transaction_id} risk score = {risk_score}")

    except Transaction.DoesNotExist:

        print(f"Transaction {transaction_id} not found")

    return True