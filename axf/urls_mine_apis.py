from django.conf.urls import url
from .mine_apis import UserInfoRetrieveAPIView
urlpatterns = [
    url(r"^userinfo$", UserInfoRetrieveAPIView.as_view()),
]