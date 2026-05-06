from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from AIapp.models import Transaction
from AIapp.risk.risk_engine import RiskEngine


@shared_task
def send_otp_task(user_id, code):
    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject="Your verification code",
            message=f"Your OTP code is: {code}\n\nValid for 5 minutes.",
            from_email="noreply@aibanking.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"OTP sent to {user.email}")
    except Exception as e:
        print(f"OTP send error: {e}")
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