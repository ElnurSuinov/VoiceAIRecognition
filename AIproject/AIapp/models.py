from django.db import models
from django.contrib.auth.models import User

class DialogueLog(models.Model):
    user_text = models.TextField()
    intent = models.CharField(max_length=50)
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} | {self.intent}"


class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=500)

    def __str__(self):
        return f"{self.name} - {self.balance} pounds"


class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    target_account = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} to {self.target_account} at {self.created_at}"