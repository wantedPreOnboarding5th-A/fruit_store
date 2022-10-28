from user.repository import UserRepo
from provider.auth_provider import auth_provider


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepo()

    def create(
        self, email: str, password: str, name: str, phone_number: str, user_type: str
    ) -> dict:
        password = auth_provider.hashpw(password)
        created_user = self.repo.create(
            name=name,
            email=email,
            password=password,
            phone_number=phone_number,
            user_type=user_type,
        )
        return created_user
