from fruit_store.enums import BaseEnum


class SaleStatusType(BaseEnum):
    WAIT = "W"  # 판매 대기
    OUT_OF_STOCK = "O"  # 재고 없음
    SALE = "S"  # 판매 중
