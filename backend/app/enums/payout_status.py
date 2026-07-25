from enum import StrEnum


class PayoutStatus(StrEnum):
    PENDING = "PENDING"
    HOLD = "HOLD"
    PROCESSING = "PROCESSING"
    PAID = "PAID"
    FAILED = "FAILED"