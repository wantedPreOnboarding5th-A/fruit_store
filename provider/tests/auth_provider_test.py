from provider.auth_provider import AuthProvider
import pytest

auth_provider = AuthProvider()


def test_create_token():
    sut = auth_provider.create_token()
    assert isinstance(sut, dict)
