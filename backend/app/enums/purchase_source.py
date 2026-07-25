from enum import Enum


class PurchaseSource(str, Enum):
    LISTING = "LISTING"
    OFFER = "OFFER"
    AUCTION = "AUCTION"
    RESERVATION = "RESERVATION"