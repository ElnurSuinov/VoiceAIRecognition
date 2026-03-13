from AIapp.models import AuditLog


class AuditLogger:

    @staticmethod
    def log(user, event_type, metadata=None):
        AuditLog.objects.create(
            user=user,
            event_type=event_type,
            metadata=metadata or {}
        )