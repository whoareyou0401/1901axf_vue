from django.conf.urls import url
from .order_apis import *
urlpatterns = [
    url(r"^order$", OrderAPI.as_view()),
]