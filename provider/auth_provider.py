from user.repository import UserRepo
import jwt
from django.conf import settings
from exceptions import (
    NoPermssionError,
    NotFoundError,
    NotFoundUserError,
    NotAuthorizedError,
)
from user.enums import UserType

user_repo = UserRepo()


class AuthProvider:
    def __init__(self):
        self.key = settings.JWT_KEY

    def create_token(self, user_id: str):
        encoded_jwt = jwt.encode({"id": user_id}, self.key, algorithm="HS256")
        return {"access": encoded_jwt}

    def login(self, email: str, password: str):
        try:
            user = user_repo.get_by_email_and_pwd(email=email, password=password)
            return self.create_token(user["id"])
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise NotFoundUserError()
            else:
                raise e

    def check_auth(self, token: str) -> bool:
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        try:
            user = user_repo.get(decoded["id"])
            if user:
                return user
            else:
                raise NotAuthorizedError
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise NotAuthorizedError

    def check_is_admin(self, token: str):
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        user = user_repo.get(decoded["id"])
        if user["user_type"] == UserType.ADMIN.value:
            return True
        else:
            raise NoPermssionError


auth_provider = AuthProvider()
