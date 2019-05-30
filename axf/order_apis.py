import datetime

import shortuuid
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import OrderSerializer
from .auth import LoginAuthentication
from .models import *

class OrderAPI(ListCreateAPIView):
    authentication_classes = [LoginAuthentication]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
    #     获取参数
        user = request.user
# 1 去购物车找用户选中的商品数据
        carts = Cart.objects.filter(
            user=user,
            c_is_select=True
        )
        if not carts.exists():
            return Response({
                "code": 10,
                "msg": "您未选中任何商品，无法下单"
            })
        # 2 创建个订单 时间
        time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        number_str = time_str + shortuuid.uuid()
        order = Order.objects.create(
            number=number_str,
            user=user,
            status=1
        )

    # 3遍历我们购物车内选中商品循环创建订单详情
        for i in carts:
            order_item = OrderItem.objects.create(
                order=order,
                goods=i.c_goods,
                num=i.c_goods_num,
                final_price=int(i.c_goods.price * 100)
            )

    # 4告诉前端订单信息让用户确认订单
        serializer = self.serializer_class(order)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        user = request.user
        status = request.query_params.get("status")
        queryset = self.queryset.filter(
            user=user, status=status
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        user_order_queryset = queryset.filter(
            user=user, status=status
        )
        serializer = self.get_serializer(user_order_queryset, many=True)
        unselect_orders = user_order_queryset.filter(is_select=False)
        if not unselect_orders.exists() and user_order_queryset.exists():
            is_all_select = True
        else:
            is_all_select = False
        sum_money = 0
        for i in user_order_queryset.filter(is_select=True):
            # i 表示的是每一个订单 通过反向关系（orderitems） 获取订单对应订单详情
            for j in i.orderitems.all():
                sum_money += (j.num * j.final_price)

        result = {
            "is_all_select": is_all_select,
            "select_order_sum_money": sum_money,
            "detail": serializer.data
        }
        return Response({"data": result})