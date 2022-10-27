from order.service import PaymentService
import pytest
from django.conf import settings

payment_service = PaymentService()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_pay():
    sut = payment_service.pay(order_id=1, payment_type="N", amount=1000)
    assert isinstance(sut, dict)
