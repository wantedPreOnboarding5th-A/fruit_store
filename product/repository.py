from .models import Product, ProductDescription, ProductImg
from .serilaizers import ProductSerializer, ProductDetailSerializer

class ProductRepo:
    def __init__(self) -> None:
        self.model = Product
        self.serilaizer = ProductSerializer

    def get(self) -> dict:
        return self.serilaizer(self.model.objects.all()).data

    def upsert(self, data: dict) -> dict:
        obj, created = self.model.objects.update_or_create(
            defaults=data,
        )
        return self.serilaizer(obj).data

class ProductDetailRepo:
    def __init__(self) -> None:
        self.model = ProductDescription
        self.serilaizer = ProductDetailSerializer

    def get(self, product_id: int) -> dict:
        return self.serilaizer(self.model.objects.get(id=product_id)).data