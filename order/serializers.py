from rest_framework import serializers

from order.models import Order, OrderDeilivery, OrderPayment, OrderTransaction, ProductOut

"""
직렬화를 담당
Order, OrderPayment, OrderDelivery, ProductOut

Detail page에 들어갈 정보 -> 단일만 조회  = OrderTransaction, OrderPayments

조회시 일부 컬럼만 리스트로 직렬화 -> Order, #To-do
"""

"""
단일 Order
"""


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


"""
출고 테이블
"""


class ProductOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOut
        fields = "__all__"


"""
배송정보
"""


class OrderDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeilivery
        fields = "__all__"
