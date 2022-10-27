from order.repository import OrderDeliveryRepo, OrderRepo, PaymentRepo, ProductOutRepo, TransactionRepo
from order.serializers import PayReqSchema, PayResSchema
from order.enums import TransactionStatusType, PaymentType
from order.exceptions import AlreadyPaidError, PaymentRequestFailed
from provider.payment_provider import CardPayProvider, NaverPayProvider
from utils.dict_helper import exclude_by_keys

payment_repo = PaymentRepo()
transaction_repo = TransactionRepo()


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
        return transaction["status"] == TransactionStatusType.PAID_FINISHED.value

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
        transaction = exclude_by_keys(
            set(["id", "created_at", "updated_at"]), transaction
        )
        d = {**data, **payment, **transaction}
        serializer = PayResSchema(data=d)
        serializer.is_valid(raise_exception=True)
        return serializer.data

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

        # 이미 성공한 결제인지 확인
        is_already_paid = self._validate_payemnt_is_paid(order_id)
        if is_already_paid:
            raise AlreadyPaidError

        # payment에 따른 provider 호출
        payment_provider = self.payment_porvider_map[payment_type]
        is_success, response = payment_provider.request_pay(order_id, amount)

        transaction_status = self._get_payment_status(is_success)

        # TODO: payment와 transaction upsert atomic 보장
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
            return self._parse_payment_with_transaction(
                transaction=transaction, payment=payment
            )
        else:
            # 결제 요청이 실패한 경우 request가 실패한 것으로 간주, db에 결과 반영 후 에러 response
            raise PaymentRequestFailed

order_repo = OrderRepo()
order_delivery_repo = OrderDeliveryRepo()
product_out_repo = ProductOutRepo()


        """
        작업흐름 : 주문생성(결제대기) -> 결제완료(업데이트) ->출고요청(업데이트)
                   ->출고완료(배송중) -> 이하는 배송 Status 꾸준히 업데이트
        """
        
class OrderManagementService:
    
    #Validation 체크 : 상품 출고
    """
    단일 품목으로 주문받는경우 수량은 productOut options에서 끌어오기
    product repo에서 상품을 끌어오기 
    
    폼별로 따로 들어온다고 가정하고 모델별 서비스 작성.
    """
    def order_create_(product_id: int, data):
        
    def order_create_by_cart():
    
    def deilvery_update()
    
        
    