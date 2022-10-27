from rest_framework import serializers

from .models import Product, ProductDescription, ProductImg, Cart
from order.models import Order

"""
상품 정보 테이블
"""


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDescription
        field = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImg
        field = "__all__"


class ProductRegisterSchema(serializers.Serializer):
    """
    상품 등록 및 상세 조회 기능 요청에 필요한 파라미터 정의
    """

    name = serializers.CharField(max_length=80)
    desc_context = serializers.CharField(
        max_length=1024
    )  # serializers에 TextField가 존재하지 않음
    package = serializers.CharField(max_length=50)
    producer = serializers.CharField(max_length=100)
    product_date = serializers.DateField()
    expire_date = serializers.DateField()
    law_info = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    storage_method = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=100)
    thumbnail = serializers.CharField(max_length=255)
    detail_img = serializers.JSONField()


class ProductResSchema(serializers.Serializer):
    """
    상품 리스트 조회 기능의 응답에 필요한 파라미터 정의
    """

    name = serializers.CharField(max_length=80)
    sale_status = serializers.CharField(max_length=1)
    is_sale = serializers.IntegerField()
    price = serializers.IntegerField()  # serializers에 PositiveIntegerField가 존재하지 않음


"""
장바구니 정보 테이블
"""


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
