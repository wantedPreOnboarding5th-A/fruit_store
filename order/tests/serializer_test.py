import pytest
from order.service import PayReqSchema
from rest_framework import serializers
from order.enums import PaymentType


invalid_pqy_req_schema_data = [
    {
        "order_id": 1,
        "payment_type": "X",  # invlaid type
        "amount": 1000,
    },
    {
        "order_id": 1,
        "payment_type": PaymentType.DEPOSIT.value,  # payment type deposit require more params
        "amount": 1000,
    },
    {"order_id": 1, "payment_type": PaymentType.CARD.value, "amount": -1},
]


@pytest.mark.parametrize("param", invalid_pqy_req_schema_data)
def test_create_wanted_with_invalid_params(param):
    with pytest.raises(serializers.ValidationError):
        schema = PayReqSchema(data=param)
        schema.is_valid(raise_exception=True)
