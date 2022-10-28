import pytest
from django.conf import settings
from product.repository import (
    ProductRepo,
    ProductDescriptionRepo,
    ProductImgRepo,
    ProductOptionRepo,
)
from product.enums import SaleStatusType

product_repo = ProductRepo()
product_description_repo = ProductDescriptionRepo()
product_img_repo = ProductImgRepo()
product_option_repo = ProductOptionRepo()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


"""ProductRepo 테스트"""

vaild_upsert_data = {
    "name": "김테스트",
    "sale_status": SaleStatusType.SALE.value,
    "is_sale": 0,
    "desc_context": "desc_context 테스트",
}


@pytest.mark.django_db()
def test_get_product_repo():
    sut = product_repo.get()
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_get_by_product_id_product_repo():
    sut = product_repo.get_by_product_id(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_upsert_product_repo():
    sut = product_repo.upsert()
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_delete_product_repo():
    sut = product_repo.delete(1)
    isinstance(sut, dict)


"""ProductDescriptionRepo 테스트"""

vaild_upsert_data = {
    "package": "1번, 2번, 3번 1kg, 2kg, 3kg",
    "producer": "이테이스",
    "product_date": "",  # DateField는 어떤 형식으로 요청해야 하는가?
    "expire_date": "",  # DateField는 어떤 형식으로 요청해야 하는가?
    "law_info": "테스트 관련 법 공지",
    "description": "테스트 상품 구성",
    "storage_method": "냉장 보관",
    "contact": "상품상세 참조",
}


@pytest.mark.django_db()
def test_get_by_product_id_product_description_repo():
    sut = product_description_repo.get_by_product_id(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_upsert_product_discription_repo():
    sut = product_description_repo.upsert()  # TODO data 추가 필요
    isinstance(sut, dict)


"""ProductImgRepo 테스트"""

vaild_upsert_data = {
    "thumbnail": "테스트 이미지 URL",
    "detail_img": {"테스트 이미지 URL 1": "테스트 이미지 URL", "테스트 이미지 URL 2": "테스트 이미지 URL"},
}


@pytest.mark.django_db()
def test_get_product_img_repo():
    sut = product_img_repo.get()
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_get_by_product_id_product_img_repo():
    sut = product_img_repo.get_by_product_id(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_upsert_product_img_repo():
    sut = product_img_repo.upsert()  # TODO data 추가 필요
    isinstance(sut, dict)


"""ProductOptionRepo 테스트"""

vaild_upsert_data = {
    "options": {"1번 옵션": "1번", "2번 옵션": "2번", "3번 옵션": "3번"},
    "price": {"1번 옵션": 10000, "2번 옵션": 20000, "3번 옵션": 30000},
}


@pytest.mark.django_db()
def test_get_product_option_repo():
    sut = product_option_repo.get()
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_get_by_product_id_product_option_repo():
    sut = product_option_repo.get_by_product_id(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_upsert_product_option_repo():
    sut = product_option_repo.upsert()  # TODO data 추가 필요
    isinstance(sut, dict)
