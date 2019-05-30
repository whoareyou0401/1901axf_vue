from django.conf.urls import url
from .order_apis import *
urlpatterns = [
    url(r"^order$", OrderAPI.as_view()),
    url(r"^confirm$", ConfirmOrder.as_view({"post":"confirm"})),
]