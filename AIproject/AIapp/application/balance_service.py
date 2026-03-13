from django.contrib.auth.models import User
from AIapp.infrastructure.repositories.account_repository import AccountRepository


class BalanceService:

    def __init__(self):
        self.accounts = AccountRepository()

    def get_balance(self, user: User):

        return self.accounts.get_balance(user)