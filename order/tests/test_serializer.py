from order.serializers import OrderDeliverySerializer, OrderSerializer


# refference : https://github.com/encode/django-rest-framework/blob/master/tests/test_serializer.py

# definition이 안되는 문제


class TestSerializer:
    def test_order_serializer(self):
        self.order_serializer = OrderSerializer
        order_serializer = self.order_serializer(
            data={"user_id": 1, "price": 123, "delivery_fee": 123, "status": "D"}
        )
        assert order_serializer.is_valid()
        assert order_serializer.validated_data == {
            "user_id": 1,
            "price": 123,
            "delivery_fee": 123,
            "status": "D",
        }
        assert order_serializer.data == {
            "user_id": 1,
            "price": 123,
            "delivery_fee": 123,
            "status": "D",
        }
        assert order_serializer.errors == {}

    def test_order_delivery_serializer(self):
        self.order_delivery_serializer = OrderDeliverySerializer
        order_delivery_serializer = OrderDeliverySerializer(
            data={
                "order_id": 1,
                "customer_name": "name",
                "customer_phone": "01012341234",
                "customer_email": "example123@email.com",
                "delivery_name": "name",
                "delivery_phone": "01012341234",
                "delivery_memo": "memo",
                "zip_code": "12344",
                "adress": "adress",
                "adress_detail": "adress_detail",
            }
        )

        assert order_delivery_serializer.is_valid()
        assert order_delivery_serializer.validated_data == {
            "order_id": 1,
            "customer_name": "name",
            "customer_phone": "01012341234",
            "customer_email": "example123@email.com",
            "delivery_name": "name",
            "delivery_phone": "01012341234",
            "delivery_memo": "memo",
            "zip_code": "12344",
            "adress": "adress",
            "adress_detail": "adress_detail",
        }
        assert order_delivery_serializer.data == {
            "order_id": 1,
            "customer_name": "name",
            "customer_phone": "01012341234",
            "customer_email": "example123@email.com",
            "delivery_name": "name",
            "delivery_phone": "01012341234",
            "delivery_memo": "memo",
            "zip_code": "12344",
            "adress": "adress",
            "adress_detail": "adress_detail",
        }
        assert order_delivery_serializer.errors == {}
