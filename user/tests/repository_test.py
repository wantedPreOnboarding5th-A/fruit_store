import pytest
from django.conf import settings
from user.repository import UserRepo

user_repo = UserRepo()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.mark.django_db()
def test_create_user_with_invalid_user_type():
    sut = user_repo.create(
        **{
            "name": "test",
            "email": "test@test.com",
            "phone_number": "01000000000",
            "password": "test_pwd",
            "user_type": "F",
        }
    )
    isinstance(sut, dict)
