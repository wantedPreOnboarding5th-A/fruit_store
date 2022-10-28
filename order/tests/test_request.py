from django.test import TestCase
from rest_framework.request import Request

from rest_framework.test import APIRequestFactory


factory = APIRequestFactory()


class TestInitializer(TestCase):
    def test_request_type(self):
        request = Request(factory.get("/orders/"))

        message = (
            "The `request` argument must be an instance of "
            "`django.http.HttpRequest`, not `rest_framework.request.Request`."
        )
        with self.assertRaisesMessage(AssertionError, message):
            Request(request)
