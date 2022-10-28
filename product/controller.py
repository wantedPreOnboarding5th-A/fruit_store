import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import must_be_user

from .service import ProductService, CartService
from .serilaizers import ProductRegisterSchema
from exceptions import NotFoundError
from user.models import User
from .exceptions import NotExistQueryParmeter, InvaildKey
from decorators.auth_handler import must_be_admin

product_service = ProductService()
cart_service = CartService()


class ProcuctAPI(APIView):
    def get(self, request, product_id):
        return JsonResponse(product_service.get_detail(product_id=product_id))

    @must_be_admin()
    def post(self, request):
        params = ProductRegisterSchema(data=request.data)
        params.is_valid(raise_exception=True)
        return JsonResponse(product_service.create(**params.data))

    @must_be_admin()
    def put(self, request, product_id):
        params = ProductRegisterSchema(data=request.data)
        params.is_valid(raise_exception=True)
        return JsonResponse(product_service.update(product_id=product_id, **params.data))

    @must_be_admin()
    def delete(self, request, product_id):
        return JsonResponse(product_service.delete(product_id=product_id))


@api_view(["GET"])
@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request):
    return JsonResponse(product_service.get_list())


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
        return JsonResponse(cart_service.show_items(user), safe=False, status=status.HTTP_200_OK)

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

        if not product_ids:
            raise InvaildKey()

        # 유저의 장바구니에 있는 상품에 대한 id값
        cart_num = [str(cart.product.id) for cart in user.cart_set.all()]

        # 쿼리파라미터값이 cart_num에 있는지 유효성 검사
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

        # 쿼리파라미터를 받음
        product_id = request.GET.get("product_id")

        if not product_id:
            raise InvaildKey()

        # 유저의 장바구니에 있는 상품에 대한 id값
        cart_num = [str(cart.product.id) for cart in user.cart_set.all()]

        # 쿼리파라미터값이 cart_num에 있는지 유효성 검사
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

        # 리스트 형태로 쿼리파라미터를 받음
        product_ids = request.GET.getlist("product_ids")

        if not product_ids:
            raise InvaildKey()

        # 유저의 장바구니에 있는 상품에 대한 id값
        cart_num = [str(cart.product.id) for cart in user.cart_set.all()]

        # 쿼리파라미터값이 cart_num에 있는지 유효성 검사
        for id in product_ids:
            if id not in cart_num:
                raise NotExistQueryParmeter()

        delete_cart = cart_service.delete_items(user, product_ids)

        return JsonResponse(delete_cart, status=status.HTTP_200_OK, safe=False)

    except User.DoesNotExist:
        raise NotFoundError
