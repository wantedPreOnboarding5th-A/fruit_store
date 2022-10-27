from .models import Product, ProductDescription, ProductImg, Cart
from .serilaizers import (
    ProductSerializer,
    ProductDetailSerializer,
    ProductImageSerializer,
    CartSerializer,
    OrderSerializer
)
from exceptions import NotFoundError
from rest_framework.exceptions import ValidationError

class ProductRepo:
    def __init__(self) -> None:
        self.model = Product
        self.serilaizer = ProductSerializer

    def get(self) -> dict:
        return self.serilaizer(self.model.objects.all()).data

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,  # default의 의미??
        )
        return self.serilaizer(obj).data

    def delete(self, product_id: int):
        entity = self.model.objects.get(id=product_id)
        entity.delete()
        return True

    def get_by_product_id(self, product_id: int) -> dict:
        return self.serilaizer(self.model.objects.get(id=product_id)).data


class ProductDetailRepo:
    def __init__(self) -> None:
        self.model = ProductDescription
        self.serilaizer = ProductDetailSerializer

    def get(self, product_id: int) -> dict:
        return self.serilaizer(self.model.objects.get(id=product_id)).data

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serilaizer(obj).data

    def delete(self, product_id: int):
        entity = self.model.objects.get(id=product_id)
        entity.delete()
        return True


class ProductImageRepo:
    def __init__(self) -> None:
        self.model = ProductImg
        self.serilaizer = ProductImageSerializer

    def get(self) -> dict:
        return self.serilaizer(self.model.objects.all()).data

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serilaizer(obj).data

    def delete(self, product_id: int):
        entity = self.model.objects.get(id=product_id)
        entity.delete()
        return True

    def get_by_product_id(self, product_id: int) -> dict:
        return self.serilaizer(self.model.objects.get(id=product_id)).data


class CartPepo:
    def __init__(self):
        self.serilaizer = CartSerializer
        self.model = Cart
        self.orderserilaier = OrderSerializer
    
    def get(self, user_id):
        try:
            return self.serilaizer(self.model.objects.get(user= user_id).all()).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, product_id : list):
        
        carts = [Cart.objects.get(product = Product.objects.get(id = i)) for i in product_id]
        
        
        for cart in carts:
            data = {
                "user" : cart.user,
                "price":cart.price,
                "dilivery_fee":0 if cart.price >= 50000 else 5000,
                "status":"F"
            }
            serialize = self.orderserilaier(data)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            return serialize.data

    def update(self, product_id, params):
        try:
            target = self.model.objects.get(id = product_id)
            if target.user != params["user"]:
                raise ValidationError("You can't update cart")
            serializer = self.serilaizer(target, data = params, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise NotFoundError
        return serializer.data

    def delete(self, product_ids: list):
        try:
            for product_id in product_ids:    
                target = self.model.objects.get(id =product_id )
                target.delete()
            
            return True         
        except self.model.DoesNotExist:
            raise NotFoundError

