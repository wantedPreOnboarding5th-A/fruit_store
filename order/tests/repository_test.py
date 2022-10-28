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


@pytest.mark.django_db()
def test_upsert_transcation():
    sut = transaction_repo.upsert(
        1, {"payment_id": 1, "status": "F", "amount": 1, "result_code": {"a": 1}}
    )
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_get_payment_with_transaction():
    sut = payment_repo.get_payment_with_transaction(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_find_payment_with_transaction_by_user_id():
    sut = payment_repo.find_payment_with_transaction_by_user_id(1)
    isinstance(sut, list)
    if len(sut):
        isinstance(sut[0], dict)
