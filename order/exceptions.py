from rest_framework import status
from exceptions import CustomBaseExecption


class AlreadyPaidError(CustomBaseExecption):
    def __init__(self):
        self.msg = "This order is already paid."
        self.status = status.HTTP_400_BAD_REQUEST


class PaymentRequestFailed(CustomBaseExecption):
    def __init__(self):
        self.msg = "Third party payment api request failed"
        self.status = status.HTTP_400_BAD_REQUEST
