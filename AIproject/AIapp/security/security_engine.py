class SecurityEngine:

    def can_transfer(self, user, amount):

        if not user.is_authenticated:
            return False

        if amount > 20000:
            return False

        return True

    def requires_2fa(self, amount):

        return amount > 5000