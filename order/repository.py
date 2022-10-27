from order.serializers import OrderSerializer, ProductOutSerializer
from order.models import Order, ProductOut

# Must To-do List형에 대해
# Must To-do 전역 Exception 클래스 파일 들어오면 Exception 처리
# Question : payments, Transaction

"""
OrderRepository
"""


class OrderRepo:
    def ___init___(self) -> None:
        self.model = Order
        self.serializer = OrderSerializer

        """
        user_id 를 인자로 받아 리스트를 반환
        """

    def get(self, user_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=user_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        Read Order 
        """

    def get(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

    def create(self, params: dict) -> dict:
        """create order : 인자로 딕셔너리를 받습니다."""
        Serializer = self.serializer(data=params)
        Serializer.is_valid(raise_exception=True)  # 유효성 체크
        Serializer.save()

    def update(self, order_id: int, params: dict) -> dict:
        """update order : 인자로 orderid, 딕셔너리를 받습니다.
        업데이트 하고자 하는 id가 동일하지 않은경우 에러 발생
        """
        try:
            entity = self.model.objects.get(id=order_id)
            # To-do 유효성 체크 업데이트 하고자 하는 id 작성
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

    def delete(
        self,
        order_id: int,
    ):
        """하위 엔티티에 전부 on_delete=models.CASCADE 가 걸려있으므로
        다른 모델에는 delete 를 작성하지 않았음"""
        try:
            entity = self.model.objects.get(id=order_id)
            entity.delete()
            return True
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"


"""
Product 출고 Repo
"""


class ProductOutRepo:
    def ___init___(self) -> None:
        self.model = ProductOut
        self.serializer = ProductOutSerializer

        # 출고현황을 리스트로 출력해주는 api가 필요할까 (요구사항에는 없다.)
        # self.list_serializer = OrderListSerializer

        """
        Read OrderProduct by order_id
        """

    def getByOrderId(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"
        """
        Read OrderProduct by Product_id
        """

    def getByOrderId(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        create Order
        """

    def create(self, params: dict) -> dict:
        Serializer = self.serializer(data=params)
        Serializer.is_valid(raise_exception=True)  # 유효성 체크
        Serializer.save()

        """
        update Order
        """

    def update(self, order_id: int, params: dict) -> dict:
        try:
            entity = self.model.objects.get(id=order_id)
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"


class OrderDeliveryRepo:
    def ___init___(self) -> None:
        self.model = Order
        self.serializer = OrderSerializer
        self.list_serializer = OrderListSerializer

        """
        Read OrderDelivery 
        """

    def get(self, order_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=order_id)).data
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        create Order
        """

    def create(self, params: dict) -> dict:
        Serializer = self.serializer(data=params)
        Serializer.is_valid(raise_exception=True)  # 유효성 체크
        Serializer.save()

        """
        update Order
        """

    def update(self, order_id: int, params: dict) -> dict:
        try:
            entity = self.model.objects.get(id=order_id)
            serializer = self.serializer(entity, data=params, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"

        """
        Delete Order
        """

    def delete(
        self,
        order_id: int,
    ):
        try:
            entity = self.model.objects.get(id=order_id)
            entity.delete()
            return True
        except self.model.DoesNotExist:
            raise  # Excepion class Not def yet "not exist"
