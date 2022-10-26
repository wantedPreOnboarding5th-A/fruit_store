from rest_framework import serializers
from order.models import OrderPayment, OrderTransaction
from order.enums import PaymentType, CashReciptsType


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
