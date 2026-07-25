from enum import Enum


class PayoutStatus(str, Enum):
    PENDING = "PENDING"
    HOLD = "HOLD"
    PROCESSING = "PROCESSING"
    PAID = "PAID"
    FAILED = "FAILED"