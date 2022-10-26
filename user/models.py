from django.db import models
from fruit_store.models import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    password = models.CharField(max_length=255, null=False)
    user_type = models.CharField(null=False, max_length=1, default="C")

    class Meta:
        db_table = "user"
