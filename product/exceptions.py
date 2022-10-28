from rest_framework import status
from exceptions import CustomBaseExecption


class NegativePriceError(CustomBaseExecption):
    def __init__(self):
        self.msg = "The amount cannot be negative."
        self.status = status.HTTP_400_BAD_REQUEST


class NotExistQueryParmeter(CustomBaseExecption):
    def __init__(self):
        self.msg = "The Product ID does not exist."
        self.status = status.HTTP_400_BAD_REQUEST
