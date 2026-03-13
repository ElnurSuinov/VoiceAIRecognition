class BankingException(Exception):
    """Base exception for banking domain"""
    pass


class TransferException(BankingException):
    """Generic transfer exception"""
    pass


class InsufficientFundsException(TransferException):
    pass


class SecurityViolationException(TransferException):
    pass


class RiskRejectedException(TransferException):
    pass


class TwoFactorRequiredException(TransferException):
    pass


class TwoFactorFailedException(TransferException):
    pass


class TransactionStateException(TransferException):
    pass