from django.contrib.auth.models import User
from AIapp.infrastructure.repositories.account_repository import AccountRepository


class TransactionService:

    def __init__(self):
        self.accounts = AccountRepository()

    def get_recent_transactions(self, user: User):

        return self.accounts.get_recent_transactions(user)