from django.db.models import Avg
from AIapp.models import Transaction


class BehaviorEngine:

    def evaluate(self, user, amount):

        avg_amount = Transaction.objects.filter(
            account__user=user
        ).aggregate(avg=Avg("amount"))["avg"]

        if not avg_amount:
            return 0

        deviation = float(amount) / float(avg_amount)

        if deviation > 5:
            return 40
        elif deviation > 3:
            return 25
        elif deviation > 2:
            return 10

        return 0