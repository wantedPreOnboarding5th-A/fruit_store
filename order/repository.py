from rest_framework.exceptions import ValidationError
from order.models import OrderPayment, OrderTransaction
from order.serilaizers import PaymentSerializer, TransactionSerializer
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
