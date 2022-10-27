from rest_framework import status
from exceptions import CustomBaseExecption


class NegativePriceError(CustomBaseExecption):
    def __init__(self):
        self.msg = "The amount cannot be negative."
        self.status = status.HTTP_400_BAD_REQUEST
