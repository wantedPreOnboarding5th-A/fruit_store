import enum
import string
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
from product.repository import CartRepo
from provider.payment_provider import CardPayProvider, NaverPayProvider
from utils.dict_helper import exclude_by_keys
from provider.auth_provider import auth_provider
from exceptions import NoPermssionError

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

        # ?????? ????????? ???????????? ??????
        is_already_paid = self._validate_payemnt_is_paid(order_id)
        if is_already_paid:
            raise AlreadyPaidError()

    def get(self, payment_id: int, user_id: int, auth_token: str):
        is_admin = auth_provider.check_is_admin(auth_token, no_execption=True)
        payment = payment_repo.get_payment_with_transaction(payment_id)
        payment_user_id = payment.pop("user_id")

        # ????????? ????????? ????????? ?????? ??????
        if is_admin or payment_user_id == user_id:
            return payment
        else:
            raise NoPermssionError

    def find(self, user_id: int):
        return payment_repo.find_payment_with_transaction_by_user_id(user_id)

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

        # validate ????????? raise Exception
        self._validate_pay(order_id=order_id)

        # payment??? ?????? provider ??????
        payment_provider = self.payment_porvider_map[payment_type]
        is_success, response = payment_provider.request_pay(order_id, amount)
        transaction_status = self._get_payment_status(is_success)

        # TODO: payment??? transaction upsert atomic ??????
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
            # ?????? ????????? ????????? ?????? request??? ????????? ????????? ??????, db ???????????? ????????? ?????? response
            raise PaymentRequestFailedError()


order_repo = OrderRepo()
order_delivery_repo = OrderDeliveryRepo()
product_out_repo = ProductOutRepo()
cart_repo = CartRepo()


class OrderManagementService:
    def __init__(self) -> None:
        # TODO ?????? ??????

        # Validation ?????? : ?????? ??????
        """
        ?????? ???????????? ?????????????????? ????????? productOut options?????? ????????????
        product repo?????? ????????? ????????????
        """

    # upsert ??????
    def _create_order(
        self,
        user_id: int,
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
        price ??? ????????? ?????? ????????????. ?????????????????? ??????.
        ?????? ????????? ?????? ??????
        """
        # todo ???????????? ????????? ???????????? params : user_id
        # TODO delivery ??????
        data = {
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

        total_price = 0
        total_delivery_fee = 0
        cart_list = cart_repo.find_by_user_id(user_id)

        for cart in cart_list:
            # price , options[amount]
            price = cart["price"] * cart["options"]["amount"]
            total_price = total_price + price

        for cart in cart_list:
            total_delivery_fee = total_delivery_fee + cart["delivery_fee"]

        # TODO Dilivery fee ?????? ????????????.

        # ???????????? ???????????? ??????

        order = {
            "user": user_id,
            "price": total_price,
            "delivery_fee": total_delivery_fee,
            "status": "C",  # status ??????
        }
        order_id = order_repo.create(order)["id"]

        order_delivery = {
            "order": order_id,
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
        order_delivery_repo.create(order_delivery)
        # status

        # response
        return order

    def _get_order_detail(self, order_id) -> dict:
        get_order = order_repo.get_by_order_id(order_id=order_id)
        get_delivery = order_delivery_repo.get(order_id=order_id)

        get_data = {
            "order_id": get_order["id"],
            "price": get_order["price"],
            "delivery_fee": get_order["delivery_fee"],
            "status": get_order["status"],
            # ????????? ??????????????? ????????? ??????
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

        return res.data

    def _get_order_list(user_id: int) -> list:
        """user_id ??? ????????? ????????? ?????? ????????? ??????????????? ??????"""
        """????????? ???????"""
        pass

    def _deilvery_status_update(self, order_id: int, new_status: enum) -> dict:

        order = order_repo.get_by_order_id(order_id=order_id)

        order_status_now = order["status"]
        # enum validation ??????

        order["status"] = new_status
        order_repo.update(order_id=order_id, params=order)

        return order
