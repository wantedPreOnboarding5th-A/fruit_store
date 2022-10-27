from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import User

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(  # User 생성
            email=validated_data["email"],
            username=validated_data["name"],
        )
        user.set_password(validated_data["password"])

        user.save()
        return user