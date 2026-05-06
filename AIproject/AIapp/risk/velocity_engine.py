from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q
from AIapp.models import Transaction


class VelocityEngine:

    def evaluate(self, user):
        now = timezone.now()

        result = Transaction.objects.filter(
            account__user=user,
            created_at__gte=now - timedelta(days=1)
        ).aggregate(
            day_count=Count("id"),
            hour_count=Count(
                "id",
                filter=Q(created_at__gte=now - timedelta(hours=1))
            )
        )

        score = 0
        if result["hour_count"] > 5:
            score += 30
        if result["day_count"] > 20:
            score += 40

        return score