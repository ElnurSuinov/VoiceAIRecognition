from AIapp.models import Transaction


class MetricsService:

    def total_transfers(self):
        return Transaction.objects.count()