from user.models import User
from user.serializers import UserSerializer
from exceptions import NotFoundError


class UserRepo:
    def __init__(self) -> None:
        self.model = User
        self.serializer = UserSerializer

    def get(self, user_id: int) -> dict:
        try:
            return UserSerializer(self.model.objects.get(id=user_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_email_and_pwd(self, email: str, password: str):
        try:
            return UserSerializer(
                self.model.objects.get(email=email, password=password)
            ).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(
        self, name: str, email: str, phone_number: str, password: str, user_type: str
    ):
        serializer = self.serializer(
            data={
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "password": password,
                "user_type": user_type,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
