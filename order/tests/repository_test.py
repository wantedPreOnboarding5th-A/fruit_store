import pytest
from django.conf import settings
from order.repository import TransactionRepo, PaymentRepo

transaction_repo = TransactionRepo()
payment_repo = PaymentRepo()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_get_payment():
    sut = payment_repo.get(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_get_transaction_by_order_id():
    sut = transaction_repo.get_by_order_id(1)
    isinstance(sut, dict)
