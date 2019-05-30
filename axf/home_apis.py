from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .models import *
from .serializers import *

class IndexAPI(ViewSet):

    @action(methods=["get"], detail=False)
    def list(self, request):
        # 去缓存查数据
        data = cache.get("sb_home")
        if data:
            return Response({"data": data})

        # 各种查数据
        main_wheels = Wheel.objects.all()
        main_navs = Nav.objects.all()
        main_mustbuys = MustBuy.objects.all()
        main_shops = Shop.objects.all()
        main_shows = MainShow.objects.all()
        result = {
            "main_wheels": WheelSerializer(main_wheels, many=True).data,
            "main_navs": NavSerializer(main_navs, many=True).data,
            "main_mustbuys": MustBuySerializer(main_mustbuys, many=True).data,
            "main_shops": ShopSerializer(main_shops, many=True).data,
            "main_shows":MainShowSerializer(main_shows, many=True).data
        }

        # 加入缓存
        cache.set("sb_home", result, 60)

        return Response({"data": result})