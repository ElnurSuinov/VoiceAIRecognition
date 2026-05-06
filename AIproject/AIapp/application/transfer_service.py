from django.db import transaction as db_transaction
from django.db.models import F
from django.db import IntegrityError
from django.contrib.auth.models import User

from AIapp.infrastructure.repositories.account_repository import AccountRepository
from AIapp.infrastructure.logging.audit_logger import AuditLogger

from AIapp.security.security_engine import SecurityEngine
from AIapp.security.two_factor import TwoFactorService

from AIapp.domain.transaction_lifecycle import TransactionLifecycle

from AIapp.models import Transaction, BankAccount

from AIapp.tasks import fraud_check_task

from AIapp.application.exceptions import (
    InsufficientFundsException,
    SecurityViolationException,
    TwoFactorFailedException,
    TransactionStateException
)


class TransferService:

    def __init__(self):

        self.repo = AccountRepository()
        self.security = SecurityEngine()
        self.two_factor = TwoFactorService()
        self.audit = AuditLogger()

    @db_transaction.atomic
    def execute(
        self,
        user: User,
        amount,
        target_account_number: str,
        idempotency_key: str | None = None
    ):

        # -------------------------------
        # Idempotency protection
        # -------------------------------
        if idempotency_key:

            existing = (
                Transaction.objects
                .filter(idempotency_key=idempotency_key)
                .only("id")
                .first()
            )

            if existing:

                return {
                    "message": "Duplicate request ignored.",
                    "transaction_id": existing.pk
                }

        # -------------------------------
        # Lock sender account
        # -------------------------------
        sender_account: BankAccount = (
            BankAccount.objects
            .select_for_update()
            .get(user=user)
        )

        if sender_account.balance < amount:

            self.audit.log(
                user=user,
                event_type="TRANSFER_FAILED_INSUFFICIENT_FUNDS",
                metadata={"amount": str(amount)}
            )

            raise InsufficientFundsException("Insufficient funds.")

        # -------------------------------
        # Create transaction
        # -------------------------------
        try:

            transaction_obj = Transaction.objects.create(
                account=sender_account,
                amount=amount,
                target_account=target_account_number,
                status="CREATED",
                idempotency_key=idempotency_key
            )

        except IntegrityError:

            existing = Transaction.objects.get(
                idempotency_key=idempotency_key
            )

            return {
                "message": "Duplicate request ignored.",
                "transaction_id": existing.pk
            }

        self.audit.log(
            user=user,
            event_type="TRANSFER_INITIATED",
            metadata={
                "amount": str(amount),
                "target": target_account_number
            }
        )

        # -------------------------------
        # SECURITY CHECK
        # -------------------------------

        TransactionLifecycle.transition(
            transaction_obj,
            "SECURITY_CHECK"
        )

        if not self.security.can_transfer(user, amount):
            TransactionLifecycle.transition(
                transaction_obj,
                "FAILED"
            )

            self.audit.log(
                user=user,
                event_type="TRANSFER_BLOCKED_SECURITY",
                metadata={"amount": str(amount)}
            )

            raise SecurityViolationException(
                "Transfer blocked by security policy."
            )

        # -------------------------------
        # RISK CHECK
        # -------------------------------

        TransactionLifecycle.transition(
            transaction_obj,
            "RISK_CHECK"
        )

        fraud_check_task.delay(transaction_obj.pk)

        # -------------------------------
        # Risk-based 2FA
        # -------------------------------

        requires_2fa = self.security.requires_2fa(amount)

        if requires_2fa:
            TransactionLifecycle.transition(
                transaction_obj,
                "2FA_PENDING"
            )

            code = self.two_factor.generate(transaction_obj)

            self.audit.log(
                user=user,
                event_type="TRANSFER_2FA_REQUIRED",
                metadata={"transaction_id": transaction_obj.pk}
            )


            return {
                "message": "2FA verification required.",
                "transaction_id": transaction_obj.pk
            }

        # -------------------------------
        # Finalize transfer
        # -------------------------------
        self._finalize_transfer(transaction_obj)

        return {
            "message": "Transfer completed successfully.",
            "transaction_id": transaction_obj.pk
        }

    @db_transaction.atomic
    def confirm_2fa(self, transaction_id: int, user_code: str):

        transaction_obj: Transaction = (
            Transaction.objects
            .select_for_update()
            .get(id=transaction_id)
        )

        if transaction_obj.status == "COMPLETED":

            return "Transaction already completed."

        if transaction_obj.status != "2FA_PENDING":

            raise TransactionStateException(
                "Transaction is not awaiting 2FA."
            )

        try:

            self.two_factor.verify(
                transaction_obj,
                user_code
            )

        except TwoFactorFailedException as e:

            TransactionLifecycle.transition(
                transaction_obj,
                "FAILED"
            )

            self.audit.log(
                user=transaction_obj.account.user,
                event_type="TRANSFER_2FA_FAILED",
                metadata={"transaction_id": transaction_id}
            )

            raise e

        self._finalize_transfer(transaction_obj)

        return "Transfer completed successfully."

    def _finalize_transfer(self, transaction_obj: Transaction):

        sender_account: BankAccount = (
            BankAccount.objects
            .select_for_update()
            .get(id=transaction_obj.account.id)
        )

        if sender_account.balance < transaction_obj.amount:

            TransactionLifecycle.transition(
                transaction_obj,
                "FAILED"
            )

            raise InsufficientFundsException(
                "Balance changed. Insufficient funds."
            )

        sender_account.balance = F("balance") - transaction_obj.amount
        sender_account.save(update_fields=["balance"])

        sender_account.refresh_from_db()

        TransactionLifecycle.transition(
            transaction_obj,
            "APPROVED"
        )

        TransactionLifecycle.transition(
            transaction_obj,
            "COMPLETED"
        )

        self.audit.log(
            user=sender_account.user,
            event_type="TRANSFER_COMPLETED",
            metadata={
                "amount": str(transaction_obj.amount),
                "target": transaction_obj.target_account
            }
        )