from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .auth import LoginAuthentication
from .models import *
from .serializers import CartItemSerializer
from .utils import get_total_price

class CartItemViewSet(ViewSet):

    authentication_classes = [LoginAuthentication]

    @action(methods=["post"], detail=False)
    def add_item_to_cart(self, request):
        # 首先我要知道用户
        user = request.user
        # 找到对应的商品
        goodsid = request.data.get("goodsid")
        goods = Goods.objects.get(pk=goodsid)
        # 想知道库存
        # 先判断库存
        if goods.storenums < 1:
            return Response({"code": 4, "msg": "您购买的商品暂无库存"})

        # 看看用户是不是第一次把东西放到购物车
        cart_items = Cart.objects.filter(user=user, c_goods=goods)
        # 如果是第一次： 创建购物车数据
        if not cart_items.exists():
            Cart.objects.create(
                user=user,
                c_goods=goods,
                c_goods_num=1
            )
        else:
            # 如果不是，找到对应商品的购物车数据
            # 在原来的基础上加1（购买的数量）
            cart_item = cart_items.first()
            cart_item.c_goods_num += 1
            cart_item.save()
        return Response({"msg": "添加成功"})

    @action(methods=["post"], detail=False)
    def sub_item_to_cart(self, request):
        # 首先我要知道用户
        user = request.user
        # 找到对应的商品
        goods_id = request.data.get("goodsid")
        # goods = Goods.objects.get(pk=goods_id)

        #  找购物车有没有记录
        cart_items = Cart.objects.filter(
            user=user,
            c_goods_id=goods_id
        )
        # 判断购物车里面有没有要减的数据
        if cart_items.exists():
            cart_item = cart_items.first()
            # 直接减
            cart_item.c_goods_num -= 1
            # 如果减到0了，删掉对应的数据（记个日志谁什么时间把什么东西删除掉了，每天定时统计当天用户删除商品的数量）
            if cart_item.c_goods_num == 0:
                cart_item.delete()
            else:
                cart_item.save()

            return Response({})
        else:
            return Response({"code": 20, "msg": "购物车无此商品"})


class CartAPI(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartItemSerializer
    # 需要登录的认证 保证用户是登录的
    authentication_classes = [LoginAuthentication]
    def list(self, request, *args, **kwargs):
        user = request.user

        queryset = self.get_queryset().filter(user=user)

        serializer = self.get_serializer(queryset, many=True)
        un_select_data = queryset.filter(c_is_select=False)
        # 判断全选的状态
        if queryset.exists() and not un_select_data.exists():
            is_select_all = True
        else:
            is_select_all = False
        result = {
            "carts": serializer.data,
            "total_price": get_total_price(user.id),
            "is_select_all": is_select_all
        }
        return Response({"data": result})


class CartItemStatus(UpdateAPIView):

    authentication_classes = [LoginAuthentication]

    def put(self, request, *args, **kwargs):
        # 解析id
        cid = request.data.get("cid")
        # 找数据
        cart_item = Cart.objects.get(pk=cid)
        # 将选中状态置反
        cart_item.c_is_select = not cart_item.c_is_select
        # 保存状态
        cart_item.save()
        return Response({})

class CartAllItemStatus(UpdateAPIView):

    authentication_classes = [LoginAuthentication]

    def put(self, request, *args, **kwargs):
        # 解析的是全选状态，用户
        user = request.user
        select_status = request.data.get("all_select")
        # 先判断用户是不是车里有商品
        cart_items = Cart.objects.filter(
            user=user
        )
        if cart_items.exists():
            # 如果当前解析到的是全都选中，那么对应的操作是全都不选中
            if select_status == True:
                cart_items.update(c_is_select=False)
            else:
                # 如果当前解析到的是全都不选中，那么对应的操作是全都选中
                cart_items.update(c_is_select=True)
            return Response({})
        else:
            return Response({"msg": "您未添加任何商品", "code": 30})


class CartItemAPIView(UpdateAPIView):
    authentication_classes = [LoginAuthentication]

    def put(self, request, *args, **kwargs):
        # 解析参数
        # user = request.user
        cid = request.data.get("cid")
        action = request.data.get("action")
        cart_item = Cart.objects.get(pk=cid)
        if action == "add":
            if cart_item.c_goods.storenums <= 0:
                return Response({
                    "code": 31,
                    "msg": "库存不足"
                })
            cart_item.c_goods_num += 1
            cart_item.save()
        else:
            # 在原来基础上
            # 减掉1
            cart_item.c_goods_num -= 1
            # 减到0的时候删除数据
            if cart_item.c_goods_num == 0:
                cart_item.delete()
                # 发个信号
            else:
                cart_item.save()
        return Response({})