from django.conf.urls import url
from .user_apis import *
urlpatterns = [
    url(r"^register$", UserActionViewSet.as_view({"post": "register"})),
    url(r"^login$", UserActionViewSet.as_view({"post": "login"})),
]