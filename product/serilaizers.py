from rest_framework import serializers

from .models import Product, ProductDescription

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        field = "__all__"

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDescription
        field = "__all__"

class ProductRegisterSchema(serializers.Serializer):
    """
    서비스의 상품 등록 기능 요청에 필요한 파라미터 정의
    """

    name = serializers.CharField(max_length=80)
    desc_context = serializers.CharField() # serializers에 TextField가 존재하지 않음
    package = serializers.CharField(max_length=50)
    producer = serializers.CharField(max_length=100)
    product_date = serializers.DateField()
    expire_date = serializers.DateField()
    law_info = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    storage_method = serializers.CharField(max_length=100)
    contact = serializers.CharField(max_length=100)
