from fruit_store.enums import BaseEnum


class UserType(BaseEnum):
    ADMIN = "A"  # 관리자
    CUSTOMER = "C"  # 고객
