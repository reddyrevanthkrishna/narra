from enum import Enum


class SellerType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    RETAILER = "RETAILER"