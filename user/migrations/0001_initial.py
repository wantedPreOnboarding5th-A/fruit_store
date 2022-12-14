# Generated by Django 4.1.2 on 2022-10-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=20)),
                ("email", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=11)),
                ("password", models.CharField(max_length=255)),
                ("user_type", models.CharField(default="C", max_length=1)),
            ],
            options={
                "db_table": "user",
            },
        ),
    ]
