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

    def get_list(self) -> dict:
        try:
            products = self.model.objects.all()

            res = [
                {
                    "id": product.id,
                    "name": product.name,
                    "sale_status": product.sale_status,
                    "is_sale": product.is_sale,
                    "price": product.productoption_set.get().price,
                    "thumbnail": product.productimg_set.get().thumbnail,
                }
                for product in products
            ]

            return {"res": res}
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            product = self.model.objects.get(id=product_id)
            product_options = ProductOption.objects.filter(product_id=product_id)

            options = [
                {
                    "options": option.options,
                    "price": option.price,
                }
                for option in product_options
            ]

            res = {
                "id": product.id,
                "name": product.name,
                "sale_status": product.sale_status,
                "is_sale": product.is_sale,
                "desc_context": product.desc_context,
                "options_price": options,
                "package": product.productdescription_set.get().package,
                "producer": product.productdescription_set.get().producer,
                "product_date": product.productdescription_set.get().product_date,
                "expire_date": product.productdescription_set.get().expire_date,
                "law_info": product.productdescription_set.get().law_info,
                "description": product.productdescription_set.get().description,
                "storage_method": product.productdescription_set.get().storage_method,
                "contact": product.productdescription_set.get().contact,
                "thumbnail": product.productimg_set.get().thumbnail,
                "detail_img": product.productimg_set.get().detail_img,
            }

            return res
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, data: dict) -> dict:
        created = self.model.objects.create(
            name=data["name"],
            sale_status=data["sale_status"],
            is_sale=data["is_sale"],
            desc_context=data["desc_context"],
        )
        return created

    def update(self, data: dict, product_id: int) -> dict:
        updated = self.model.objects.filter(id=product_id).update(
            name=data["name"],
            sale_status=data["sale_status"],
            is_sale=data["is_sale"],
            desc_context=data["desc_context"],
        )
        return updated

    def delete(self, product_id: int):
        entity = self.model.objects.get(id=product_id)
        entity.delete()
        return "delete"


class ProductDescriptionRepo:
    def __init__(self) -> None:
        self.model = ProductDescription
        self.serializer = ProductDescriptionSerializer

    def create(self, data: dict) -> dict:
        created = self.model.objects.create(
            product_id=data["product_id"],
            package=data["package"],
            producer=data["producer"],
            product_date=data["product_date"],
            expire_date=data["expire_date"],
            law_info=data["law_info"],
            description=data["description"],
            storage_method=data["storage_method"],
            contact=data["contact"],
        )
        return self.serializer(created).data

    def update(self, data: dict, product_id: int) -> dict:
        updated = self.model.objects.filter(id=product_id).update(
            product_id=data["product_id"],
            package=data["package"],
            producer=data["producer"],
            product_date=data["product_date"],
            expire_date=data["expire_date"],
            law_info=data["law_info"],
            description=data["description"],
            storage_method=data["storage_method"],
            contact=data["contact"],
        )
        return updated


class ProductImgRepo:
    def __init__(self) -> None:
        self.model = ProductImg
        self.serializer = ProductImgSerializer

    def create(self, data: dict) -> dict:
        created = self.model.objects.create(
            product_id=data["product_id"],
            thumbnail=data["thumbnail"],
            detail_img=data["detail_img"],
        )
        return self.serializer(created).data

    def update(self, data: dict, product_id: int) -> dict:
        updated = self.model.objects.filter(id=product_id).update(
            product_id=data["product_id"],
            thumbnail=data["thumbnail"],
            detail_img=data["detail_img"],
        )
        return updated


class ProductOptionRepo:
    def __init__(self) -> None:
        self.model = ProductOption
        self.serializer = ProductOptionSerializer

    def create(self, data: dict) -> dict:
        created = self.model.objects.create(
            product_id=data["product_id"],
            options=data["options"],
            price=data["price"],
        )
        return self.serializer(created).data

    def update(self, data: dict, product_id: int) -> dict:
        updated = self.model.objects.filter(id=product_id).update(
            product_id=data["product_id"],
            options=data["options"],
            price=data["price"],
        )
        return updated


class CartRepo:
    def __init__(self) -> None:
        self.serilaizer = CartSerializer
        self.model = Cart
        self.orderserilaier = OrderSerializer

    def find_by_user_id(self, user_id):
        try:
            return self.serilaizer(self.model.objects.filter(user_id=user_id), many=True).data

        except self.model.DoesNotExist:
            raise NotFoundError

    def find(self, user: object):
        try:
            return self.serilaizer(self.model.objects.filter(user=user), many=True).data

        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, user: object, product_ids: list) -> None:
        try:

            # 유저의 product_id에 해당하는 장바구니 객체
            carts = [
                Cart.objects.get(product=Product.objects.get(id=i), user=user) for i in product_ids
            ]

            for cart in carts:
                data = {
                    "user": cart.user.id,
                    "price": cart.price,
                    "delivery_fee": 0 if cart.price >= 50000 else 5000,  # 50000원 이상 결제시 배송비 무료
                    "status": OrderStatusType.PAID_CONFIRMD.value,  # order로 변경시 상태 코드 변경
                }
                serialize = self.orderserilaier(data=data)
                serialize.is_valid(raise_exception=True)
                serialize.save()
                cart.delete()  # order된 상품을 장바구니에서 제거

        except Cart.DoesNotExist:
            raise NotFoundError()

    def update(self, user: object, product_id: int, data: dict) -> None:
        try:
            target = self.model.objects.get(product=Product.objects.get(id=product_id), user=user)
            serializer = self.serilaizer(target, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except self.model.DoesNotExist:
            raise NotFoundError

    def delete(self, user: object, product_ids: list) -> None:
        try:
            for product_id in product_ids:
                target = self.model.objects.get(
                    product=Product.objects.get(id=product_id), user=user
                )
                target.delete()

        except self.model.DoesNotExist:
            raise NotFoundError
