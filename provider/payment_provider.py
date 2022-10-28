from django.conf import settings

# 네이버 페이, 카드 결제, 무통장 입금 클래스 구현
class NaverPayProvider:
    def __init__(self):
        self.client_id = settings.NAVER_PAY_CLIENT_ID
        self.mode = settings.NAVER_PAY_MODE
        self.merchantUserKey = settings.NAVER_PAY_MERCHANT_USER_KEY
        self.merchantPayKey = settings.NAVER_PAY_MERCHANT_PAY_KEY
        self.success_res = {"code": "Success", "message": "", "body": dict()}

    def request_pay(self, order_id: int, amount: int) -> set:
        response = self.success_res
        is_success = response["code"] == "Success"
        return is_success, response


class CardPayProvider:
    def __init__(self) -> None:
        self.member_id = settings.CARD_PAY_MEMBER_ID
        self.success_res = {"resultCode": 201, "resultMsg": "payment success"}

    def request_pay(self, order_id: int, amount: int) -> set:
        response = self.success_res
        is_success = response["resultCode"] == 201
        return is_success, response
