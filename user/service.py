from user.repository import UserRepo


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepo()

    def create(self, email, password, name, phone_number, user_type):
        created_user = self.repo.create(
            name=name,
            email=email,
            password=password,
            phone_number=phone_number,
            user_type=user_type,
        )
        return created_user
