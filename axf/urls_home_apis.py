from django.conf.urls import url
from .home_apis import IndexAPI
urlpatterns = [
    url(r"^index$", IndexAPI.as_view({"get": "list"})),
]