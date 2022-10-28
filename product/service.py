from product.repository import (
    CartPepo,
    ProductRepo,
    ProductDescriptionRepo,
    ProductImgRepo,
    ProductOptionRepo,
)
from .serilaizers import ProductRegisterSchema
from .exceptions import NegativePriceError

cartrepo = CartPepo()


class ProductService:
    """상품 CRUD관련 service layer"""

    def __init__(self) -> None:
        self.product_repo = ProductRepo()
        self.product_description_repo = ProductDescriptionRepo()
        self.product_img_repo = ProductImgRepo()
        self.product_option_repo = ProductOptionRepo()

    def _validate_price_is_positive(self, price: int):
        """상품의 가격 데이터를 받아 '-'일 경우 에러 반환"""
        if price < 0:
            raise NegativePriceError()

    def create(
        self,
        name: str,
        sale_status: str,
        is_sale: int,
        desc_context: str,
        options: str,
        price: int,
        package: str,
        producer: str,
        product_date: str,
        expire_date: str,
        law_info: str,
        description: str,
        storage_method: str,
        contact: str,
        thumbnail: str = None,
        detail_img: dict = None,
    ) -> dict:
        """상품 등록에 필요한 모든 데이터를 받아 사움 생성 및 기존 데이터 수정"""
        data = {
            "name": name,
            "sale_status": sale_status,
            "is_sale": is_sale,
            "desc_context": desc_context,
            "options": options,
            "price": price,
            "package": package,
            "producer": producer,
            "product_date": product_date,
            "expire_date": expire_date,
            "law_info": law_info,
            "description": description,
            "storage_method": storage_method,
            "contact": contact,
            "thumbnail": thumbnail,
            "detail_img": detail_img,
        }

        params = ProductRegisterSchema(data=data)
        params.is_valid(raise_exception=True)

        self._validate_price_is_positive(price=price)

        product = {
            "name": name,
            "sale_status": sale_status,
            "is_sale": is_sale,
            "desc_context": desc_context,
        }
        created = self.product_repo.create(product)

        product_option = {
            "product_id": created.id,
            "options": options,
            "price": price,
        }
        self.product_option_repo.create(product_option)

        product_description = {
            "product_id": created.id,
            "package": package,
            "producer": producer,
            "product_date": product_date,
            "expire_date": expire_date,
            "law_info": law_info,
            "description": description,
            "storage_method": storage_method,
            "contact": contact,
        }
        self.product_description_repo.create(product_description)

        product_image = {
            "product_id": created.id,
            "thumbnail": thumbnail,
            "detail_img": detail_img,
        }
        self.product_img_repo.create(product_image)

        return {"msg": "success"}

    def update(
        self,
        product_id: int,
        name: str,
        sale_status: str,
        is_sale: int,
        desc_context: str,
        options: str,
        price: int,
        package: str,
        producer: str,
        product_date: str,
        expire_date: str,
        law_info: str,
        description: str,
        storage_method: str,
        contact: str,
        thumbnail: str = None,
        detail_img: dict = None,
    ) -> dict:
        """상품 등록에 필요한 모든 데이터를 받아 사움 생성 및 기존 데이터 수정"""
        data = {
            "name": name,
            "sale_status": sale_status,
            "is_sale": is_sale,
            "desc_context": desc_context,
            "options": options,
            "price": price,
            "package": package,
            "producer": producer,
            "product_date": product_date,
            "expire_date": expire_date,
            "law_info": law_info,
            "description": description,
            "storage_method": storage_method,
            "contact": contact,
            "thumbnail": thumbnail,
            "detail_img": detail_img,
        }

        params = ProductRegisterSchema(data=data)
        params.is_valid(raise_exception=True)

        self._validate_price_is_positive(price=price)

        product = {
            "name": name,
            "sale_status": sale_status,
            "is_sale": is_sale,
            "desc_context": desc_context,
        }
        self.product_repo.update(product, product_id=product_id)

        product_option = {
            "product_id": product_id,
            "options": options,
            "price": price,
        }
        self.product_option_repo.update(product_option, product_id=product_id)

        product_description = {
            "product_id": product_id,
            "package": package,
            "producer": producer,
            "product_date": product_date,
            "expire_date": expire_date,
            "law_info": law_info,
            "description": description,
            "storage_method": storage_method,
            "contact": contact,
        }
        self.product_description_repo.update(product_description, product_id=product_id)

        product_image = {
            "product_id": product_id,
            "thumbnail": thumbnail,
            "detail_img": detail_img,
        }
        self.product_img_repo.update(product_image, product_id=product_id)

        return {"msg": "success"}

    def get_list(self) -> dict:
        """상품 리스트 페이지에 표시해야할 데이터 반환"""
        return self.product_repo.get_list()

    def get_detail(self, product_id: int) -> dict:
        """상품 id값을 받아 상세 페이지에 표시해야할 데이터 반환"""
        return self.product_repo.get_by_product_id(product_id=product_id)

    def delete(self, product_id: int):
        """상품 id값을 받아 삭제"""
        return {"msg": self.product_repo.delete(product_id=product_id)}


class CartService:
    def __init__(self):
        pass

    def show_all_carts_items(self, user_id):
        return cartrepo.get(user_id)

    def pay_cart_items(self, product_id=[]):
        return JsonResponse(cartrepo.create(product_id))

    def update_cart_items(self, product_id, params):
        return JsonResponse(cartrepo.update(product_id, params))

    def delete_cart_items(self, product_ids=[]):
        return JsonResponse(cartrepo.delete(product_ids))
