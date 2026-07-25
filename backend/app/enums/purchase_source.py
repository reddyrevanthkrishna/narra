from enum import StrEnum


class PurchaseSource(StrEnum):
    LISTING = "LISTING"
    OFFER = "OFFER"
    AUCTION = "AUCTION"
    RESERVATION = "RESERVATION"