import pytest
from django.conf import settings

from product.service import ProductService
from product.enums import SaleStatusType

product_service = ProductService

vaild_create_or_update_data = {
    "name": "김테스트",
    "sale_status": SaleStatusType.SALE.value,
    "is_sale": 0,
    "desc_context": "desc_context 테스트",
    "options": {"1번 옵션": "1번", "2번 옵션": "2번", "3번 옵션": "3번"},
    "price": {"1번 옵션": 10000, "2번 옵션": 20000, "3번 옵션": 30000},
    "package": "1번, 2번, 3번 1kg, 2kg, 3kg",
    "producer": "이테이스",
    "product_date": "",  # DateField는 어떤 형식으로 요청해야 하는가?
    "expire_date": "",  # DateField는 어떤 형식으로 요청해야 하는가?
    "law_info": "테스트 관련 법 공지",
    "description": "테스트 상품 구성",
    "storage_method": "냉장 보관",
    "contact": "상품상세 참조",
    "thumbnail": "테스트 이미지 URL",
    "detail_img": {"테스트 이미지 URL 1": "테스트 이미지 URL", "테스트 이미지 URL 2": "테스트 이미지 URL"},
}


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_pay():
    sut = product_service.create_or_update(vaild_create_or_update_data)
    assert isinstance(sut, dict)
