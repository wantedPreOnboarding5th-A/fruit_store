from rest_framework import serializers

from order.models import Order, OrderDeilivery, OrderPayment, OrderTransaction, ProductOut

"""
직렬화를 담당
Order, OrderPayment, OrderDelivery, ProductOut

Detail page에 들어갈 정보 -> 단일만 조회  = OrderTransaction, OrderPayments

조회시 일부 컬럼만 리스트로 직렬화 -> Order, #To-do
"""
# Question : Serialize에서 DB의 엔티티를 조회시 하위 엔티티들은 어떻게 처리되는가.
# Question : Serialize 할때 필드명을 명시하는게 좋은가
# Question : Order에는 Total fee, Total Price (장바구니 합계를 저장)
# Question :

"""
단일 Order
"""


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


"""
Delivery Status for Order List
"""


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"  # To-do 리스트로 조회시 필드명 정리


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
