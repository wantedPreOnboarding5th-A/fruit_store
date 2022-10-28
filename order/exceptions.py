from rest_framework import status
from exceptions import CustomBaseExecption


class AlreadyPaidError(CustomBaseExecption):
    def __init__(self):
        self.msg = "This order is already paid."
        self.status = status.HTTP_400_BAD_REQUEST


class PaymentRequestFailedError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Third party payment api request failed"
        self.status = status.HTTP_400_BAD_REQUEST


class CanNotPayNonExistOrderError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Cant not pay non exist order"
        self.status = status.HTTP_400_BAD_REQUEST
