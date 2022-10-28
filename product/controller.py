import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import must_be_user

from .service import ProductService, CartService
from .serilaizers import ProductRegisterSchema, ProductListSchema
from exceptions import NotFoundError
from user.models import User
from .exceptions import NotExistQueryParmeter


product_service = ProductService()
cart_service = CartService()


@api_view(["POST"])
@execption_hanlder()
@parser_classes([JSONParser])
def create(request):
    params = ProductRegisterSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(product_service.create_or_update(**params.data))


@api_view(["GET"])
@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request):
    return JsonResponse(product_service.get_list())


@api_view(["GET"])
@execption_hanlder()
@parser_classes([JSONParser])
def get_detail(request):
    params = ProductRegisterSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(product_service.get_detail(**params.data))


@api_view(["DELETE"])
@execption_hanlder()
@parser_classes([JSONParser])
def delete(request):
    params = ProductListSchema(data=request.data)
    params.is_valid(raise_exception=True)
    return JsonResponse(product_service.delete(**params.data))


class CartAPI(APIView):
    def get(self, request):
        return show_cart_items(request)

    def post(self, request):
        return pay_new_product(request)

    def patch(self, request):
        return update_cart_items(request)

    def delete(self, request):
        return delete_cart_items(request)


@execption_hanlder()
@parser_classes([JSONParser])
@must_be_user()
def show_cart_items(request):
    try:
        user = User.objects.get(id=request.user["id"])
        return JsonResponse(
            cart_service.show_items(user), safe=False, status=status.HTTP_200_OK
        )

    except User.DoesNotExist:
        raise NotFoundError


@execption_hanlder()
@parser_classes([JSONParser])
@must_be_user()
def pay_new_product(request):
    try:
        user = User.objects.get(id=request.user["id"])

        # 리스트 형태로 쿼리파라미터를 받음
        product_ids = request.GET.getlist("product_ids")
        cart_num = [str(cart.product.id) for cart in user.cart_set.all()]

        for id in product_ids:
            if id not in cart_num:
                raise NotExistQueryParmeter()

        create_order = cart_service.pay_items(user, product_ids)

        return JsonResponse(create_order, status=status.HTTP_201_CREATED, safe=False)

    except User.DoesNotExist:
        raise NotFoundError


@execption_hanlder()
@parser_classes([JSONParser])
@must_be_user()
def update_cart_items(request):
    try:
        user = User.objects.get(id=request.user["id"])
        data = json.loads(request.body)

        product_id = request.GET.get("product_id")
        cart_num = [str(cart.product.id) for cart in user.cart_set.all()]

        if product_id not in cart_num:
            raise NotExistQueryParmeter()

        update_cart = cart_service.update_items(user, product_id, data)

        return JsonResponse(update_cart, status=status.HTTP_200_OK, safe=False)

    except User.DoesNotExist:
        raise NotFoundError


@execption_hanlder()
@parser_classes([JSONParser])
@must_be_user()
def delete_cart_items(request):
    try:
        user = User.objects.get(id=request.user["id"])

        product_ids = request.GET.getlist("product_ids")
        cart_num = [str(cart.product.id) for cart in user.cart_set.all()]

        for id in product_ids:
            if id not in cart_num:
                raise NotExistQueryParmeter()

        delete_cart = cart_service.delete_items(user, product_ids)

        return JsonResponse(delete_cart, status=status.HTTP_200_OK, safe=False)

    except User.DoesNotExist:
        raise NotFoundError
