from fruit_store.enums import BaseEnum


class PaymentType(BaseEnum):
    NAVER_PAY = "N"
    CARD = "C"
    DEPOSIT = "D"  # 무통장 입금


class CashReciptsType(BaseEnum):
    PERSONAL = "P"
    COMPANY = "C"


class TransactionStatusType(BaseEnum):
    PAID_FINISHED = "T"
    PAID_FAILED = "F"


class OrderStatusType(BaseEnum):
    PAID_CONFIRMD = "P"
    PAID_FALLED = "F"

    DELIVERY_STARTED = "D"
    DELIVERY_FINISHED = "Y"
    DELIVERY_FALLED = "N"
    ORDER_CANCLED = "C"
