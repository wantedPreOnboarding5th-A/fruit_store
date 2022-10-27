from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder

from .service import ProductService
from .serilaizers import ProductRegisterSchema, ProductListSchema

product_service = ProductService()


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
