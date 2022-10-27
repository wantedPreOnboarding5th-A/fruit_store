from product.repository import CartPepo
from django.http import JsonResponse

cartrepo = CartPepo()

class CartService:
    def __init__(self):
        pass


    def show_all_carts_items(self,user_id):
        return cartrepo.get(user_id)


    def pay_cart_items(self, product_id = []):
        return JsonResponse(cartrepo.create(product_id))


    def update_cart_items(self, product_id, params):
        return JsonResponse(cartrepo.update(product_id, params))

    
    def delete_cart_items(self, product_ids = []):
        return JsonResponse(cartrepo.delete(product_ids))

    