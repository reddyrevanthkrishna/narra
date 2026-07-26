from enum import StrEnum


class PaymentMethod(StrEnum):
    UPI = "UPI"
    CARD = "CARD"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"
    OTHER = "OTHER"