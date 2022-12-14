# Generated by Django 4.1.2 on 2022-10-26 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("price", models.IntegerField()),
                ("delivery_fee", models.IntegerField()),
                ("status", models.CharField(max_length=1)),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.user",
                    ),
                ),
            ],
            options={
                "db_table": "order",
            },
        ),
        migrations.CreateModel(
            name="ProductOut",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("price", models.IntegerField()),
                ("delivery_fee", models.IntegerField()),
                ("options", models.JSONField()),
                ("status", models.CharField(max_length=1)),
                ("trace_no", models.CharField(max_length=100)),
                (
                    "order",
                    models.ForeignKey(
                        db_column="order_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="order.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        db_column="product_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
            ],
            options={
                "db_table": "product_out",
            },
        ),
        migrations.CreateModel(
            name="OrderPayment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("payment_type", models.CharField(max_length=1)),
                ("cash_receipts", models.CharField(max_length=1)),
                ("cash_receipts_number", models.IntegerField()),
                ("deposit_number", models.IntegerField()),
                ("depositor", models.CharField(max_length=20)),
                (
                    "order",
                    models.ForeignKey(
                        db_column="order_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="order.order",
                    ),
                ),
            ],
            options={
                "db_table": "order_payment",
            },
        ),
        migrations.CreateModel(
            name="OrderDilivery",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("customer_name", models.CharField(max_length=20)),
                ("customer_phone", models.CharField(max_length=11)),
                ("customer_email", models.CharField(max_length=100)),
                ("delivery_name", models.CharField(max_length=20)),
                ("delivery_phone", models.CharField(max_length=100)),
                ("delivery_memo", models.CharField(max_length=100)),
                ("zip_code", models.CharField(max_length=6)),
                ("address", models.CharField(max_length=255)),
                ("address_detail", models.CharField(max_length=100)),
                (
                    "order",
                    models.ForeignKey(
                        db_column="order_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="order.order",
                    ),
                ),
            ],
            options={
                "db_table": "order_dilivery",
            },
        ),
        migrations.CreateModel(
            name="Order_transaction",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(max_length=1)),
                ("amount", models.IntegerField()),
                ("result_code", models.JSONField()),
                (
                    "payment",
                    models.ForeignKey(
                        db_column="payment_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="order.orderpayment",
                    ),
                ),
            ],
            options={
                "db_table": "order_transacton",
            },
        ),
    ]
