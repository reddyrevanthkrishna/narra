from enum import StrEnum


class PaymentGateway(StrEnum):
    RAZORPAY = "RAZORPAY"
    STRIPE = "STRIPE"
    PAYPAL = "PAYPAL"
    CASHFREE = "CASHFREE"