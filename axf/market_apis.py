from copy import deepcopy
from django.contrib.auth.models import AnonymousUser
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
import django_filters.rest_framework
from .models import FoodTypes, Goods, Cart
from .serializers import FoodTypesSerializer, GoodsSerializer
from .filters import GoodsFilter
from .auth import LoginAuthentication, LoginMiniAuthentication


class FoodTypesAPI(ListAPIView):
    queryset = FoodTypes.objects.all()
    serializer_class = FoodTypesSerializer#没有序列化器

class GoodsAPI(ListAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = GoodsFilter
    authentication_classes = [ LoginMiniAuthentication ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        # 如果用户登录 我们才有必要去查购物车数据
        user = request.user
        result_data = []
        # 如果没登录 那么就直接返回数据
        if isinstance(user, AnonymousUser):
            result_data = serializer.data
        else:
            # 去购物车找数据吧
            user_cart = Cart.objects.filter(user=user).values("c_goods_id", "c_goods_num")
            # 如果购物车有数据
            if user_cart.exists():
                # 登录了 购物车还有数据
                # goods_num_map = {}
                # for j in user_cart:
                #     goods_num_map[j.get("c_goods_id")] = j.get("c_goods_num"){495:3个}
                goods_num_map = {j.get("c_goods_id"): j.get("c_goods_num") for j in user_cart}
                for i in serializer.data:
                    i["num"] = goods_num_map.get(i.get("id"), 0)
                    result_data.append(i)
            else:
                # 登录了但是购物车没有数据
                result_data = serializer.data

        # 如果没登录
        # 返回一级分类对应的二级分类数据
        # 要知道你给我的一级分类的ID
        type_id = request.query_params.get("typeid")
        goods_type = FoodTypes.objects.get(typeid=type_id)
        sub_goods_type_str = goods_type.childtypenames
        foodtype_childname_list = []
        for i in sub_goods_type_str.split("#"):
            sub_data = i.split(":")
            tmp = {
                "child_value": sub_data[1],
                "child_name": sub_data[0]
            }
            foodtype_childname_list.append(tmp)

        order_rule_list = [
            {
                "order_value": -1,
                "order_name": "综合排序"
            },
            {
                "order_value": 0,
                "order_name": "价格升序"
            },
            {
                "order_value": 1,
                "order_name": "价格降序"
            },
            {
                "order_value": 2,
                "order_name": "销量升序"
            },
            {
                "order_value": 3,
                "order_name": "销量降序"
            }
        ]
        data = {
            "goods_list": result_data,
            "order_rule_list": order_rule_list,
            "foodtype_childname_list": foodtype_childname_list
        }
        return Response({"data":data})
