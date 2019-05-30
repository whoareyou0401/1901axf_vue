from django.conf.urls import url
from .market_apis import *
urlpatterns = [
    url(r"^foodtypes$", FoodTypesAPI.as_view()),
    url(r"^goods$", GoodsAPI.as_view()),
]