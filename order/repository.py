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
            payment = dict_fetchone(cursor)
            if payment == None:
                raise NotFoundError()
            else:
                return payment


# Must To-do List 처리
# Must To-do 전역 Exception 클래스 파일 들어오면 Exception 처리

"""
OrderRepository
"""


class OrderRepo:
    def __init__(self) -> None:
        self.model = Order
        self.serializer = OrderSerializer

        """
        user_id 를 인자로 받아 리스트를 반환
        """

    def find_order_by_user_id(self, user_id: int) -> dict:
        
        self.serializer(self.model.objects.get(id=user_id)).data
        try:
            return 
        except self.model.DoesNotExist:
            raise  NotFoundError()

        """
        Read Order 
        """

    def get_by_order_id(self, order_id: int) -> dict:

        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError()

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
            # TODO 유효성 체크 id 동일한지
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  NotFoundError()

        """
        Deprecated : Order 삭제 대신 상태 컬럼 업데이트로 변경
        """
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
            raise  NotFoundError()
    
    def find_order(
        
    )

"""
Product 출고 Repo
"""


class ProductOutRepo:
    def __init__(self) -> None:
        self.model = ProductOut
        self.serializer = ProductOutSerializer

        """
        Read OrderProduct by order_id
        """

    def get_by_order_id(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  NotFoundError()
        """
        Read OrderProduct by Product_id
        """

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise  NotFoundError()

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
            raise  NotFoundError()


class OrderDeliveryRepo:
    def __init__(self) -> None:
        self.model = Order
        self.serializer = OrderSerializer

        """
        Read OrderDelivery 
        """

    def get(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  NotFoundError()

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
            raise  NotFoundError()

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
            raise  NotFoundError()
