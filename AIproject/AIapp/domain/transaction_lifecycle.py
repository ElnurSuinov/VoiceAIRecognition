class TransactionLifecycle:

    VALID_TRANSITIONS = {
        "CREATED": ["SECURITY_CHECK"],
        "SECURITY_CHECK": ["RISK_CHECK", "FAILED"],
        "RISK_CHECK": ["2FA_PENDING", "APPROVED", "FAILED", "FROZEN"],
        "2FA_PENDING": ["APPROVED", "FAILED"],
        "APPROVED": ["COMPLETED"],
        "COMPLETED": [],
        "FAILED": [],
        "FROZEN": ["FAILED"],
    }

    @staticmethod
    def transition(transaction, new_state):
        if new_state not in TransactionLifecycle.VALID_TRANSITIONS[transaction.status]:
            raise Exception(f"Invalid transition {transaction.status} → {new_state}")
        transaction.status = new_state
        transaction.save(update_fields=["status"])
        