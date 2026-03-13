from django.utils import timezone
from datetime import timedelta
from AIapp.models import Transaction


class VelocityEngine:

    def evaluate(self, user):

        now = timezone.now()

        last_hour = now - timedelta(hours=1)
        last_day = now - timedelta(days=1)

        hour_count = Transaction.objects.filter(
            account__user=user,
            created_at__gte=last_hour
        ).count()

        day_count = Transaction.objects.filter(
            account__user=user,
            created_at__gte=last_day
        ).count()

        score = 0

        if hour_count > 5:
            score += 30

        if day_count > 20:
            score += 40

        return score