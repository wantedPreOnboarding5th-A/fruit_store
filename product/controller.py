from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from decorators.execption_handler import execption_hanlder

from .service import ProductService
from .serilaizers import ProductRegisterSchema, ProductListSchema

product_service = ProductService()


class ProcuctAPI(APIView):
    def get(self, request, product_id):
        return JsonResponse(product_service.get_detail(product_id=product_id))

    def post(self, request):
        params = ProductRegisterSchema(data=request.data)
        params.is_valid(raise_exception=True)
        return JsonResponse(product_service.create(**params.data))

    def put(self, request, product_id):
        params = ProductRegisterSchema(data=request.data)
        params.is_valid(raise_exception=True)
        return JsonResponse(product_service.update(product_id=product_id, **params.data))

    def delete(self, request, product_id):
        return JsonResponse(product_service.delete(product_id=product_id))


@api_view(["GET"])
@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request):
    return JsonResponse(product_service.get_list())
