from .models import Product, ProductDescription, ProductImg, Cart, ProductOption
from .serilaizers import (
    ProductOptionSerializer,
    ProductSerializer,
    ProductDescriptionSerializer,
    ProductImgSerializer,
    CartSerializer,
    OrderSerializer,
)
from exceptions import NotFoundError
from rest_framework.exceptions import ValidationError
from order.enums import OrderStatusType


class ProductRepo:
    def __init__(self) -> None:
        self.model = Product
        self.serializer = ProductSerializer

    def get(self) -> dict:
        try:
            return self.serializer(self.model.objects.all()).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serializer(obj).data

    def delete(self, product_id: int):
        entity = self.model.objects.get(id=product_id)
        entity.delete()
        return True


class ProductDescriptionRepo:
    def __init__(self) -> None:
        self.model = ProductDescription
        self.serializer = ProductDescriptionSerializer

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serializer(obj).data


class ProductImgRepo:
    def __init__(self) -> None:
        self.model = ProductImg
        self.serializer = ProductImgSerializer

    def get(self) -> dict:
        try:
            return self.serializer(self.model.objects.all()).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serializer(obj).data


class ProductOptionRepo:
    def __init__(self) -> None:
        self.model = ProductOption
        self.serializer = ProductOptionSerializer

    def get(self) -> dict:
        try:
            return self.serializer(self.model.objects.all()).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serializer(obj).data


class CartRepo:
    def __init__(self) -> None:
        self.serilaizer = CartSerializer
        self.model = Cart
        self.orderserilaier = OrderSerializer
    
    def find(self, user):
        try:
            return self.serilaizer(self.model.objects.filter(user=user), many = True).data
        
        except self.model.DoesNotExist:
            raise NotFoundError

    
    def create(self, user, product_id):        
        try:

            # 유저의 product_id에 해당하는 장바구니 객체  
            carts = [Cart.objects.get(product = Product.objects.get(id = i), user = user) for i in product_id]
            
            for cart in carts:
                data = {
                    "user" : cart.user.id,
                    "price":cart.price,
                    "dilivery_fee":0 if cart.price >= 50000 else 5000, # 50000원 이상 결제시 배송비 무료
                    "status": OrderStatusType.PAID_CONFIRMD.value
                }
                serialize = self.orderserilaier(data=data)
                serialize.is_valid(raise_exception=True)
                serialize.save()
                cart.delete()

        except Cart.DoesNotExist:
            raise NotFoundError() 

        
    def update(self, user, product_id, data):
        try:
            target = self.model.objects.get(product = Product.objects.get(id = product_id), user = user)
            serializer = self.serilaizer(target, data = data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
        except self.model.DoesNotExist:
            raise NotFoundError
        

    def delete(self, user, product_ids: list):
        try:
            for product_id in product_ids:    
                target = self.model.objects.get(product = Product.objects.get(id = product_id), user = user )
                target.delete()
        
        except self.model.DoesNotExist:
            raise NotFoundError 