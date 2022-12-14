from rest_framework import serializers

from order.models import (
    Order,
    OrderDeilivery,
    OrderPayment,
    OrderTransaction,
    ProductOut,
)
from order.enums import PaymentType, CashReciptsType

"""
단일 Order
"""


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateReqSchema(serializers.Serializer):
    """
    Service 기능 요청을 위한 주문 요청 scheme
    """

    # 이하는 배송정보에 들어갈 내용
    trace_no = serializers.CharField()
    customer_name = serializers.CharField()
    customer_phone = serializers.CharField()
    customer_email = serializers.CharField()
    delivery_name = serializers.CharField()
    delivery_phone = serializers.CharField()
    delivery_memo = serializers.CharField()
    zip_code = serializers.CharField()
    address = serializers.CharField()
    address_detail = serializers.CharField()


class OrderResSchema(serializers.Serializer):
    """
    Service 기능 주문 응답 scheme
    """

    order_id = serializers.IntegerField()
    price = serializers.IntegerField()

    delivery_fee = serializers.IntegerField()
    status = serializers.CharField()

    # 이하는 배송정보에 들어갈 내용
    customer_name = serializers.CharField()
    customer_phone = serializers.CharField()
    delivery_name = serializers.CharField()
    delivery_phone = serializers.CharField()
    delivery_memo = serializers.CharField()
    zip_code = serializers.CharField()
    address = serializers.CharField()
    address_detail = serializers.CharField()


class ProductOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOut
        fields = "__all__"


class OrderDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeilivery
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTransaction
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = "__all__"


class PayReqSchema(serializers.Serializer):
    """
    service의 pay 기능 요청에 필요한 파라매터 정의 입니다.
    """

    order_id = serializers.IntegerField()
    payment_type = serializers.CharField(max_length=1)
    amount = serializers.IntegerField()
    cash_receipts = serializers.CharField(max_length=1, required=False, allow_null=True)
    cash_receipts_number = serializers.IntegerField(required=False, allow_null=True)
    deposit_number = serializers.IntegerField(required=False, allow_null=True)
    depositor = serializers.CharField(max_length=20, required=False, allow_null=True)

    def validate_payment_type(self, value: str):
        if PaymentType.has_value(value):
            return value
        else:
            raise serializers.ValidationError("Unkwon payment type")

    def validate_amount(self, value: int):
        if value > 0:
            return value
        else:
            raise serializers.ValidationError("amount must be bigger than 0")

    def _validate_deposit_pay_required(self):
        if self.data["payment_type"] != PaymentType.DEPOSIT.value:
            return True
        else:
            return CashReciptsType.has_value(self.cash_receipts) and (
                None
                not in [
                    self.cash_receipts_number,
                    self.deposit_number,
                    self.depositor,
                ]
            )

    def is_valid(self, *, raise_exception=False):
        validated = super().is_valid(raise_exception=raise_exception)
        if not raise_exception:
            return validated and self._validate_deposit_pay_required()
        else:
            if self._validate_deposit_pay_required():
                return validated
            else:
                raise serializers.ValidationError(
                    "deposit require cash_receipts_number, deposit_number, depositor"
                )


class PayResSchema(serializers.Serializer):
    """
    service의 pay 기능 응답 정의 입니다.
    """

    id = serializers.IntegerField()
    transaction_id = serializers.IntegerField()
    status = serializers.CharField(max_length=1)
    amount = serializers.IntegerField()
    result_code = serializers.JSONField()
    payment_type = serializers.CharField(max_length=1)
    amount = serializers.IntegerField()
    cash_receipts = serializers.CharField(max_length=1, required=False, allow_null=True)
    cash_receipts_number = serializers.IntegerField(required=False, allow_null=True)
    deposit_number = serializers.IntegerField(required=False, allow_null=True)
    depositor = serializers.CharField(max_length=20, required=False, allow_null=True)
    updated_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField()
