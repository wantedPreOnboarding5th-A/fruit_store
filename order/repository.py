from rest_framework.exceptions import ValidationError
from order.models import OrderPayment, OrderTransaction, Order, ProductOut
from order.serializers import (
    PaymentSerializer,
    TransactionSerializer,
    OrderSerializer,
    ProductOutSerializer,
)
from exceptions import NotFoundError
from pypika import MySQLQuery, Table
from django.db import connection
from utils.pypika_helper import dict_fetchone

payment_table = Table("order_payment")
transaction_table = Table("order_transacton")


class PaymentRepo:
    def __init__(self) -> None:
        self.serilaizer = PaymentSerializer
        self.model = OrderPayment

    def get(self, payment_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(id=payment_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def upsert(self, order_id: int, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            order_id=order_id,
            defaults=data,
        )
        return self.serilaizer(obj).data


class TransactionRepo:
    def __init__(self) -> None:
        self.model = OrderTransaction
        self.serilaizer = TransactionSerializer

    def upsert(self, payment_id: int, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            payment=payment_id,
            defaults=data,
        )
        return self.serilaizer(obj).data

    def get_by_order_id(self, order_id: int) -> dict:
        get_payment_by_order_query = (
            MySQLQuery.from_(payment_table)
            .select(payment_table.id)
            .where(payment_table.order_id == order_id)
        )
        query = (
            MySQLQuery.from_(transaction_table)
            .select(transaction_table.star)
            .where(transaction_table.payment_id == get_payment_by_order_query)
        )
        with connection.cursor() as cursor:
            cursor.execute(query.get_sql())
            return dict_fetchone(cursor)


# Must To-do List 처리
# Must To-do 전역 Exception 클래스 파일 들어오면 Exception 처리

"""
OrderRepository
"""


class OrderRepo:
    def ___init___(self) -> None:
        self.model = Order
        self.serializer = OrderSerializer

        """
        user_id 를 인자로 받아 리스트를 반환
        """

    def get(self, user_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=user_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        Read Order 
        """

    def get(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

    def create(self, params: dict) -> dict:
        """create order : 인자로 딕셔너리를 받습니다."""
        Serializer = self.serializer(data=params)
        Serializer.is_valid(raise_exception=True)  # 유효성 체크
        Serializer.save()

    def update(self, order_id: int, params: dict) -> dict:
        """update order : 인자로 orderid, 딕셔너리를 받습니다.
        업데이트 하고자 하는 id가 동일하지 않은경우 에러 발생
        """
        try:
            entity = self.model.objects.get(id=order_id)
            # To-do 유효성 체크 업데이트 하고자 하는 id 작성
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

    def delete(
        self,
        order_id: int,
    ):
        """하위 엔티티에 전부 on_delete=models.CASCADE 가 걸려있으므로
        다른 모델에는 delete 를 작성하지 않았음"""
        try:
            entity = self.model.objects.get(id=order_id)
            entity.delete()
            return True
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"


"""
Product 출고 Repo
"""


class ProductOutRepo:
    def ___init___(self) -> None:
        self.model = ProductOut
        self.serializer = ProductOutSerializer

        # 출고현황을 리스트로 출력해주는 api가 필요할까 (요구사항에는 없다.)
        # self.list_serializer = OrderListSerializer

        """
        Read OrderProduct by order_id
        """

    def get_by_order_id(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"
        """
        Read OrderProduct by Product_id
        """

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        create Order
        """

    def create(self, params: dict) -> dict:
        Serializer = self.serializer(data=params)
        Serializer.is_valid(raise_exception=True)  # 유효성 체크
        Serializer.save()

        """
        update Order
        """

    def update(self, order_id: int, params: dict) -> dict:
        try:
            entity = self.model.objects.get(id=order_id)
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"


class OrderDeliveryRepo:
    def ___init___(self) -> None:
        self.model = Order
        self.serializer = OrderSerializer

        """
        Read OrderDelivery 
        """

    def get(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        create Order
        """

    def create(self, params: dict) -> dict:
        Serializer = self.serializer(data=params)
        Serializer.is_valid(raise_exception=True)  # 유효성 체크
        Serializer.save()

        """
        update Order
        """

    def update(self, order_id: int, params: dict) -> dict:
        try:
            entity = self.model.objects.get(id=order_id)
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        Delete Order
        """

    def delete(
        self,
        order_id: int,
    ):
        try:
            entity = self.model.objects.get(id=order_id)
            entity.delete()
            return True
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"
