from django.db import models
from django.contrib.auth.models import User


class DialogueLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    user_text = models.TextField()

    intent = models.CharField(
        max_length=100,
        db_index=True
    )

    ai_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f"{self.created_at} | {self.intent}"


class AuditLog(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    event_type = models.CharField(
        max_length=50,
        db_index=True
    )

    metadata = models.JSONField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f"{self.created_at} | {self.event_type}"


class BankAccount(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.balance}"


class Transaction(models.Model):

    STATUS_CHOICES = [
        ("CREATED", "Created"),
        ("SECURITY_CHECK", "Security Check"),
        ("RISK_CHECK", "Risk Check"),
        ("2FA_PENDING", "2FA Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("FROZEN", "Frozen"),
    ]

    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        db_index=True
    )

    target_account = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CREATED",
        db_index=True
    )

    risk_score = models.IntegerField(
        default=0,
        db_index=True
    )

    idempotency_key = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return f"{self.amount} | {self.status}"


class TwoFactorCode(models.Model):

    MAX_ATTEMPTS = 3

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="two_factor"
    )

    code = models.CharField(
        max_length=6
    )

    attempts = models.IntegerField(
        default=0
    )

    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"2FA for transaction {self.transaction.id}"


class DeviceFingerprint(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    device_hash = models.CharField(
        max_length=128,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} | {self.ip_address}"


class RiskRule(models.Model):

    name = models.CharField(
        max_length=100
    )

    condition = models.CharField(
        max_length=100
    )

    score = models.IntegerField()

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} ({self.score})"

class DepositProduct(models.Model):
    name = models.CharField(max_length=100)

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    term_months = models.IntegerField()

    minimum_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.name

class LoanProduct(models.Model):
    name = models.CharField(max_length=100)

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    term_months = models.IntegerField()

    minimum_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.name

class CardProduct(models.Model):
    name = models.CharField(max_length=100)

    cashback_percent = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    annual_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name