from django.conf.urls import url
from .cart_apis import *
urlpatterns = [
    url(r"^cart_add_action$", CartItemViewSet.as_view({"post":"add_item_to_cart"})),
    url(r"^cart_sub_action$", CartItemViewSet.as_view({"post":"sub_item_to_cart"})),
    url(r"^carts$", CartAPI.as_view()),
    url(r"^item_status$", CartItemStatus.as_view()),
    url(r"^all_status$", CartAllItemStatus.as_view()),
    url(r"^cart_item$", CartItemAPIView.as_view()),
]