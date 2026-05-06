from datetime import timedelta
from django.utils import timezone
import secrets

from AIapp.models import TwoFactorCode
from AIapp.application.exceptions import TwoFactorFailedException
from AIapp.tasks import send_otp_task


class TwoFactorService:

    EXPIRATION_MINUTES = 5
    MAX_ATTEMPTS = 3

    def generate(self, transaction):

        code = str(secrets.randbelow(900000) + 100000)

        expires = timezone.now() + timedelta(minutes=self.EXPIRATION_MINUTES)

        TwoFactorCode.objects.update_or_create(
            transaction=transaction,
            defaults={
                "code": code,
                "attempts": 0,
                "expires_at": expires,
                "is_verified": False
            }
        )

        send_otp_task.delay(transaction.account.user.id, code)

        return code

    def verify(self, transaction, user_code):

        try:
            two_factor = transaction.two_factor
        except TwoFactorCode.DoesNotExist:
            raise TwoFactorFailedException("No OTP generated.")

        if two_factor.is_verified:
            return True

        if timezone.now() > two_factor.expires_at:
            raise TwoFactorFailedException("OTP expired.")

        if two_factor.attempts >= self.MAX_ATTEMPTS:
            raise TwoFactorFailedException("Maximum OTP attempts exceeded.")

        if two_factor.code != user_code:
            two_factor.attempts += 1
            two_factor.save(update_fields=["attempts"])
            raise TwoFactorFailedException("Invalid OTP.")

        two_factor.is_verified = True
        two_factor.save(update_fields=["is_verified"])

        return True