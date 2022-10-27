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


class CartPepo:  # TODO 오타 수정
    def __init__(self):
        self.serilaizer = CartSerializer
        self.model = Cart
        self.orderserilaier = OrderSerializer

    def get(self, user_id):
        try:
            return self.serilaizer(self.model.objects.get(user=user_id).all()).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, product_id: list):

        carts = [Cart.objects.get(product=Product.objects.get(id=i)) for i in product_id]

        for cart in carts:
            data = {
                "user": cart.user,
                "price": cart.price,
                "dilivery_fee": 0 if cart.price >= 50000 else 5000,
                "status": "F",
            }
            serialize = self.orderserilaier(data)
            serialize.is_valid(raise_exception=True)
            serialize.save()
            return serialize.data

    def update(self, product_id, params):
        try:
            target = self.model.objects.get(id=product_id)
            if target.user != params["user"]:
                raise ValidationError("You can't update cart")
            serializer = self.serilaizer(target, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise NotFoundError
        return serializer.data

    def delete(self, product_ids: list):
        try:
            for product_id in product_ids:
                target = self.model.objects.get(id=product_id)
                target.delete()

            return True
        except self.model.DoesNotExist:
            raise NotFoundError
