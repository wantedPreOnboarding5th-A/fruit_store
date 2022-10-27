from user.repository import UserRepo
import jwt
from django.conf import settings
from exceptions import (
    NoPermssionError,
    NotFoundError,
    NotFoundUserError,
    NotAuthorizedError,
    TokenExpiredError,
)
from user.enums import UserType
from datetime import datetime
import bcrypt

user_repo = UserRepo()


class AuthProvider:
    def __init__(self):
        self.key = settings.JWT_KEY
        self.expire_sec = settings.JWT_EXPIRE_TIME

    def _get_curr_sec(self):
        return datetime.now().timestamp()

    def hashpw(self, password: str):
        return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("utf8")

    def checkpw(self, password: str, hashed: str):
        return bcrypt.checkpw(password.encode("utf8"), hashed.encode("utf8"))

    def _decode(self, token: str):
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        if decoded["exp"] <= self._get_curr_sec():
            raise TokenExpiredError
        else:
            return decoded

    def create_token(self, user_id: str, is_expired: bool = False):
        exp = 0 if is_expired else self._get_curr_sec() + self.expire_sec
        encoded_jwt = jwt.encode(
            {"id": user_id, "exp": exp},
            self.key,
            algorithm="HS256",
        )
        return {"access": encoded_jwt}

    def login(self, email: str, password: str):
        try:
            user = user_repo.get_by_email(email=email)
            if self.checkpw(password, user["password"]):
                return self.create_token(user["id"])
            else:
                raise NotFoundUserError()
        except Exception as e:
            if isinstance(e, NotFoundError):
                raise NotFoundUserError()
            else:
                raise e

    def logout(self, token: str):
        decoded = self._decode(token)
        return self.create_token(decoded["id"], is_expired=True)

    def check_auth(self, token: str) -> bool:
        decoded = self._decode(token)
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
        decoded = self._decode(token)
        user = user_repo.get(decoded["id"])
        if user["user_type"] == UserType.ADMIN.value:
            return True
        else:
            raise NoPermssionError


auth_provider = AuthProvider()
