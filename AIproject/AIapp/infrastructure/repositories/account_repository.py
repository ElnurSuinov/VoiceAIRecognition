from django.contrib.auth.models import User
from AIapp.models import BankAccount, Transaction


class AccountRepository:

    def get_account(self, user: User) -> BankAccount:
        return BankAccount.objects.get(user=user)

    def get_balance(self, user: User):

        account: BankAccount = BankAccount.objects.get(user=user)

        return account.balance

    def debit(self, user: User, amount):

        account: BankAccount = BankAccount.objects.get(user=user)

        account.balance -= amount
        account.save(update_fields=["balance"])

    def credit(self, user: User, amount):

        account: BankAccount = BankAccount.objects.get(user=user)

        account.balance += amount
        account.save(update_fields=["balance"])

    def get_recent_transactions(self, user: User, limit: int = 5):

        account: BankAccount = BankAccount.objects.get(user=user)

        return (
            Transaction.objects
            .filter(account=account)
            .order_by("-created_at")[:limit]
        )