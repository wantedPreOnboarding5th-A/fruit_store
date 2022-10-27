import enum
import json
from re import S
import string
from order import serializers
from order.repository import (
    OrderDeliveryRepo,
    OrderRepo,
    PaymentRepo,
    ProductOutRepo,
    TransactionRepo,
)
from exceptions import NotFoundError
from order.serializers import (
    OrderCreateReqSchema,
    OrderGetReqSchema,
    OrderResSchema,
    PayReqSchema,
    PayResSchema,
)
from order.enums import TransactionStatusType, PaymentType
from order.exceptions import (
    AlreadyPaidError,
    PaymentRequestFailedError,
    CanNotPayNonExistOrderError,
)
from product.repository import CartPepo
from provider.payment_provider import CardPayProvider, NaverPayProvider
import user
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
    def __init__(self) -> None:
        self.order_repo = OrderRepo()
        self.order_delivery_repo = OrderDeliveryRepo()
        self.product_out_repo = ProductOutRepo()
        self.cart_repo = CartPepo()  # TODO 오타 수정

    # Validation 체크 : 상품 출고
    """
    단일 품목으로 주문받는경우 수량은 productOut options에서 끌어오기
    product repo에서 상품을 끌어오기

    """

    def _create_order(
        self,
        user_id: int,
        delivery_fee: int,
        trace_no: string,
        customer_name: string,
        customer_phone: string,
        customer_email: string,
        delivery_name: string,
        delivery_phone: string,
        delivery_memo: string,
        zip_code: int,
        address: string,
        address_detail: string,
    ) -> dict:
        """
        price 는 인수로 받지 않습니다. 장바구니에서 계산.
        모든 권한이 접근 가능
        """
        # todo 장바구니 리스트 끌어오기 params : user_id
        # TODO delivery 수정
        data = {
            "delivery_fee": delivery_fee,
            "trace_no": trace_no,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "delivery_name": delivery_name,
            "delivery_phone": delivery_phone,
            "delivery_memo": delivery_memo,
            "zip_code": zip_code,
            "address": address,
            "address_detail": address_detail,
        }

        params = OrderCreateReqSchema(data=data)
        params.is_valid(raise_exception=True)

        # cart repo에 리스트 요청
        cart_list = self.cart_repo.get(user_id=user_id)

        # cart 가격 합산
        for cart in cart_list:
            # price , options[amount]
            price = cart["price"] * cart["options"]["amount"]
            total_price = total_price + price

        for cart in cart_list:
            total_delivery_fee = total_delivery_fee + cart["dilivery_fee"]

        # TODO Dilivery fee 수정 바랍니다.

        # 필드별로 나누어서 저장
        order = {
            "user_id": user_id,
            "price": total_price,
            "dilivery_fee": total_delivery_fee,
            "status": "C",  # status 조금
        }
        self.order_repo.create(order)

        order_delivery = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "delivery_name": delivery_name,
            "delivery_phone": delivery_phone,
            "delivery_memo": delivery_memo,
            "zip_code": zip_code,
            "address": address,
            "address_detail": address_detail,
        }
        self.order_delivery_repo.create(order_delivery)
        # status

        # response
        return order

    def _get_order_list(
        self,
        order_id,
        user_id,
    ):
        pass

    def _get_order_detail(
        self,
        order_id,
        user_id,
    ) -> dict:
        data = {"order_id": order_id, "user_id": user_id}
        data = OrderGetReqSchema(data=data)
        data.is_valid(raise_exception=True)
        # 만약 로그인한 유저가 아닐경우 검증할 로직이 필요한지
        #
        get_order = self.order_repo.get_by_order_id(order_id=order_id)
        get_delivery = self.order_delivery_repo.get(order_id=order_id)

        get_data = {
            "order_id": get_order["order_id"],
            "price": get_order["price"],
            # TODO 오타수정 delivery -> delivery
            "delivery_fee": get_order["delivery_fee"],
            "options": get_order["options"],
            "status": get_order["status"],
            "trace_no": get_delivery["trace_no"],
            # 이하는 배송정보에 들어갈 내용
            "customer_name": get_delivery["customer_name"],
            "customer_phone": get_delivery["customer_phone"],
            "delivery_name": get_delivery["delivery_name"],
            "delivery_phone": get_delivery["delivery_phone"],
            "delivery_memo": get_delivery["delivery_memo"],
            "zip_code": get_delivery["zip_code"],
            "address": get_delivery["address"],
            "address_detail": get_delivery["address_detail"],
        }
        res = OrderResSchema(data=get_data)
        res.is_valid(raise_exception=True)

        return res

    # def _get_order_list(user_id: int) -> list:
    #     pass

    def _deilvery_status_update(order_id: int, new_status: enum) -> dict:
        order = order_repo.get_by_order_id(order_id=order_id)
        order_status_now = order["status"]
        order_status_new = new_status  # enum validation 작성

        order["status"] = new_status
        order_repo.update(order_id=order["order_id"])

        res = {"order_id": order_id}
        return res
