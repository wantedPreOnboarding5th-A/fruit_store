from order.models import OrderDeilivery, OrderPayment, OrderTransaction, Order, ProductOut
from order.serializers import (
    OrderDeliverySerializer,
    PaymentSerializer,
    TransactionSerializer,
    OrderSerializer,
    ProductOutSerializer,
)
from exceptions import NotFoundError
from pypika import MySQLQuery, Table
from django.db import connection
from utils.pypika_helper import dict_fetchone, dict_fetchall

payment_table = Table("order_payment")
transaction_table = Table("order_transacton")
order_table = Table("order")


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

    def get_payment_with_transaction(self, payment_id: int) -> dict:
        query = (
            MySQLQuery.from_(payment_table)
            .select(
                payment_table.star,
                transaction_table.id.as_("transaction_id"),
                transaction_table.status,
                transaction_table.amount,
                order_table.user_id,
            )
            .where(payment_table.id == payment_id)
            .left_join(transaction_table)
            .on(payment_table.id == transaction_table.payment_id)
            .left_join(order_table)
            .on(payment_table.order_id == order_table.id)
        )
        with connection.cursor() as cursor:
            cursor.execute(query.get_sql())
            payment = dict_fetchone(cursor)
            if payment == None:
                raise NotFoundError()
            else:
                return payment

    def find_payment_with_transaction_by_user_id(self, user_id: int):
        query = (
            MySQLQuery.from_(payment_table)
            .select(
                payment_table.star,
                transaction_table.id.as_("transaction_id"),
                transaction_table.status,
                transaction_table.amount,
            )
            .left_join(transaction_table)
            .on(payment_table.id == transaction_table.payment_id)
            .left_join(order_table)
            .on(order_table.id == payment_table.order_id)
            .where(order_table.user_id == user_id)
        )
        with connection.cursor() as cursor:
            cursor.execute(query.get_sql())
            payment = dict_fetchall(cursor)
            if payment == None:
                raise NotFoundError()
            else:
                return payment


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
            raise NotFoundError()

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
        serializer = self.serializer(data=params)
        serializer.is_valid(raise_exception=True)  # 유효성 체크
        serializer.save()
        return serializer.data

    def update(self, order_id: int, params: dict) -> dict:
        """update order : 인자로 orderid, 딕셔너리를 받습니다.
        업데이트 하고자 하는 id가 동일하지 않은경우 에러 발생
        """
        try:
            entity = self.model.objects.get(id=order_id)
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise NotFoundError()


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
            raise NotFoundError()
        """
        Read OrderProduct by Product_id
        """

    def get_by_product_id(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError()

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
            raise NotFoundError()


class OrderDeliveryRepo:
    def __init__(self) -> None:
        self.model = OrderDeilivery
        self.serializer = OrderDeliverySerializer

        """
        Read OrderDelivery 
        """

    def get(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(order=order_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError()

        """
        create Order
        """

    def create(self, params: dict) -> dict:
        serializer = self.serializer(data=params)
        serializer.is_valid(raise_exception=True)  # 유효성 체크
        serializer.save()

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
            raise NotFoundError()

        """
        Delete Order
        """
