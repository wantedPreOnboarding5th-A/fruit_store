from email.policy import default
from django.db import models
from fruit_store.models import BaseModel
from user.models import User


class Product(BaseModel):
    name = models.CharField(max_length=80, null=False)
    sale_status = models.CharField(max_length=1, null=False, default="W")
    is_sale = models.IntegerField(null=False, default=0)
    desc_context = models.TextField()

    class Meta:
        db_table = "product"


class ProductDescription(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id",
    )
    package = models.CharField(max_length=50)
    producer = models.CharField(max_length=100)
    product_date = models.DateField()
    expire_date = models.DateField()
    law_info = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    storage_method = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    class Meta:
        db_table = "product_description"


class ProductImg(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id",
    )
    thumbnail = models.CharField(max_length=255)
    detail_img = models.JSONField()

    class Meta:
        db_table = "product_img"


# class Badge(BaseModel):
#     name = models.CharField(max_length=10, null=False)

#     class Meta:
#         db_table = "badge"


# class ProductBadge(BaseModel):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         db_column="product_id",
#     )
#     badge = models.ForeignKey(
#         Badge,
#         on_delete=models.CASCADE,
#         db_column="badge_id",
#     )

#     class Meta:
#         db_table = "product_badge"


class Cart(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id",
    )
    price = models.PositiveIntegerField(null=False, default=0)
    delivery_fee = models.PositiveIntegerField(null=False, default=0)
    options = models.JSONField(null=False, default=dict)

    class Meta:
        db_table = "cart"


class ProductOption(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column="product_id",
    )
    options = models.CharField(null=False, max_length=50)
    price = models.PositiveIntegerField(null=False, default=0)

    class Meta:
        db_table = "product_option"
