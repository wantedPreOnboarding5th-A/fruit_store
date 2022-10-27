from django.db import models
from user.models import User
from product.models import Product
from fruit_store.models import BaseModel


class Order(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    price = models.IntegerField(null=False)
    dilivery_fee = models.IntegerField(null=False)
    status = models.CharField(max_length=1)

    class Meta:
        db_table = "order"


class ProductOut(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column="order_id",
    )
    price = models.IntegerField(null=False)
    delivery_fee = models.IntegerField(null=False)
    options = models.JSONField(null=False)
    status = models.CharField(max_length=1, null=False)
    trace_no = models.CharField(max_length=100)

    class Meta:
        db_table = "product_out"


class OrderPayment(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column="order_id",
    )
    payment_type = models.CharField(max_length=1, null=False)
    cash_receipts = models.CharField(max_length=1)
    cash_receipts_number = models.IntegerField()
    deposit_number = models.IntegerField()
    depositor = models.CharField(max_length=20)

    class Meta:
        db_table = "order_payment"


class OrderDeilivery(BaseModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        db_column="order_id",
    )
    customer_name = models.CharField(max_length=20)
    customer_phone = models.CharField(max_length=11)
    customer_email = models.CharField(max_length=100)
    delivery_name = models.CharField(max_length=20)
    delivery_phone = models.CharField(max_length=100)
    delivery_memo = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    address = models.CharField(max_length=255)
    address_detail = models.CharField(max_length=100)

    class Meta:
        db_table = "order_dilivery"


class OrderTransaction(BaseModel):
    payment = models.ForeignKey(
        OrderPayment,
        on_delete=models.CASCADE,
        db_column="payment_id",
    )
    status = models.CharField(max_length=1)
    amount = models.IntegerField()
    result_code = models.JSONField()

    class Meta:
        db_table = "order_transacton"
