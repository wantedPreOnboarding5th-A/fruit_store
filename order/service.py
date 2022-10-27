import json
import string
from order.repository import (
    OrderDeliveryRepo,
    OrderRepo,
    PaymentRepo,
    ProductOutRepo,
    TransactionRepo,
)
from exceptions import NotFoundError
from order.serializers import OrderReqSchema, OrederReqSchema, PayReqSchema, PayResSchema
from order.enums import TransactionStatusType, PaymentType
from order.exceptions import (
    AlreadyPaidError,
    PaymentRequestFailedError,
    CanNotPayNonExistOrderError,
)
from provider.payment_provider import CardPayProvider, NaverPayProvider
from utils.dict_helper import exclude_by_keys

payment_repo = PaymentRepo()
transaction_repo = TransactionRepo()
order_repo = OrderRepo()


class PaymentService:
    def __init__(self) -> None:
        self.naver_payment_provider = NaverPayProvider()
        self.card_payment_provider = CardPayProvider()
        self.payment_porvider_map = {
            PaymentType.NAVER_PAY.value: self.naver_payment_provider,
            PaymentType.CARD.value: self.card_payment_provider,
        }

    def _validate_payemnt_is_paid(self, order_id: int) -> bool:
        transaction = transaction_repo.get_by_order_id(order_id=order_id)
        try:
            return transaction["status"] == TransactionStatusType.PAID_FINISHED.value
        except NotFoundError:
            return True

    def _get_payment_status(self, is_success: bool) -> str:
        return (
            TransactionStatusType.PAID_FINISHED.value
            if is_success
            else TransactionStatusType.PAID_FAILED.value
        )

    def _parse_payment_with_transaction(self, payment: dict, transaction: dict) -> dict:
        data = {
            "id": payment["id"],
            "transaction_id": transaction["id"],
        }
        payment.pop("order")

        transaction = exclude_by_keys(set(["id", "created_at", "updated_at"]), transaction)
        serializer = PayResSchema(data={**data, **payment, **transaction})
        serializer.is_valid(raise_exception=True)
        return serializer.data

    def _validate_order_exist(self, order_id: int) -> bool:
        try:
            order_repo.get_by_order_id(order_id)
            return True
        except Exception as e:
            if isinstance(e, NotFoundError):
                return False
            else:
                raise e

    def _validate_pay(self, order_id: int):
        is_order_exist = self._validate_order_exist(order_id=order_id)
        if not is_order_exist:
            raise CanNotPayNonExistOrderError()

        # 이미 성공한 결제인지 확인
        is_already_paid = self._validate_payemnt_is_paid(order_id)
        if is_already_paid:
            raise AlreadyPaidError()

    def pay(
        self,
        order_id: int,
        payment_type: str,
        amount: int,
        cash_receipts: str = None,
        cash_receipts_number: str = None,
        deposit_number: int = None,
        depositor: str = None,
    ):
        data = {
            "order_id": order_id,
            "payment_type": payment_type,
            "amount": amount,
            "cash_receipts": cash_receipts,
            "cash_receipts_number": cash_receipts_number,
            "deposit_number": deposit_number,
            "depositor": depositor,
        }
        params = PayReqSchema(data=data)
        params.is_valid(raise_exception=True)

        # validate 실패시 raise Exception
        self._validate_pay(order_id=order_id)

        # payment에 따른 provider 호출
        payment_provider = self.payment_porvider_map[payment_type]
        is_success, response = payment_provider.request_pay(order_id, amount)
        transaction_status = self._get_payment_status(is_success)

        # TODO: payment와 transaction upsert atomic 보장
        amount = data.pop("amount")
        payment = payment_repo.upsert(order_id, data)
        payment_id = payment["id"]
        transaction = transaction_repo.upsert(
            payment_id,
            {
                "payment_id": payment_id,
                "status": transaction_status,
                "amount": amount,
                "result_code": response,
            },
        )
        if is_success:
            return self._parse_payment_with_transaction(transaction=transaction, payment=payment)
        else:
            # 결제 요청이 실패한 경우 request가 실패한 것으로 간주, db 반영과는 별도로 에러 response
            raise PaymentRequestFailedError()


class OrderManagementService:
    order_repo = OrderRepo()
    order_delivery_repo = OrderDeliveryRepo()
    product_out_repo = ProductOutRepo()

    order_req = OrderReqSchema()

    # Validation 체크 : 상품 출고
    """
    단일 품목으로 주문받는경우 수량은 productOut options에서 끌어오기
    product repo에서 상품을 끌어오기

    """

    def _create_order(
        self,
        user_id: int,
        order_id: int,
        delivery_fee: int,
        trace_no: string,
        customer_name: string,
        customer_phone: string,
        delivery_name: string,
        delivery_phone: string,
        delivery_memo: string,
        zip_code: int,
        address: string,
        address_detail: string,
    ):
        """price 는 인수로 받지 않습니다. 장바구니에서 계산."""
        # todo 장바구니 리스트 끌어오기 params : user_id
        # dilivery -> delivery
        # Mock Data
        cart_list = [
            {
                "user_id": 1,
                "product_id": 1,
                "price": 1000,
                "dilivery_fee": 2000,
                "options": {"amount": 2},
            },
            {
                "user_id": 1,
                "product_id": 2,
                "price": 3000,
                "dilivery_fee": 3000,
                "options": {"amount": 2},
            },
        ]

        for cart in cart_list:
            # price , options[amount]
            price = cart["price"] * cart["options"]["amount"]
            total_price = total_price + price

        for cart in cart_list:
            total_delivery_fee = total_delivery_fee + cart["dilivery_fee"]

        """
        장바구니 항목 : uid 를 param 으로 product: price:...
        """
        # Todo Req schema 로 req validation
        pass

    def _get_order():

        pass

    def _deilvery_update():
        pass

    def _payment_update(self, order_id: int):

        order_repo.get_by_order_id(order_id)

    def _cancle_order():
        pass
