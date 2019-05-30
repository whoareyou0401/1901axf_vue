import datetime
import uuid

import requests
import shortuuid
import xmltodict
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

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


def sign(params, sign_key):
    params = [(str(key), str(val)) for key, val in params.items() if val]
    sorted_params_string = '&'.join('='.join(pair) for pair in sorted(params))
    sign_str = "{}&key={}".format(sorted_params_string, sign_key).encode("utf-8")
    md5 = hashlib.md5()
    md5.update(sign_str)
    return md5.hexdigest().upper()

def xml_response_to_dict(rep):
    d = xmltodict.parse(rep.content.decode())
    return dict(d['xml'])

class ConfirmOrder(ViewSet):

    authentication_classes = [LoginAuthentication]
    @action(methods=["post"], detail=False)
    def confirm(self, request):
        user = request.user
        id = request.data.get("id")
        order = Order.objects.get(id=id)
        sum_money = 0
        for i in order.orderitems.all():
            sum_money += (i.num * i.final_price)
        # 发起支付了
        # 获取IP
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            ip = request.META.get('REMOTE_ADDR')

        nonce_str = str(uuid.uuid4()).replace("-", "")
        out_trade_no = order.number
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        body = "axf".encode("utf-8")
        data = {}
        data["body"] = body
        data["appid"] = "wxxxxxxxx91a808f"
        data["nonce_str"] = nonce_str
        data["mch_id"] = "1xxxxxxxxx6702"
        data["out_trade_no"] = out_trade_no[:32]
        data["total_fee"] = sum_money
        data["spbill_create_ip"] = ip
        data["notify_url"] = "http://sharemsg.cn:12346/axf/notice"
        data["trade_type"] = "MWEB"
        data["scene_info"] = """{"h5_info": {"type":"Wap","wap_url": "https://sharemsg.cn","wap_name": "hehe"}}"""
        data["sign"] = sign(data, "sssssss")
        template = """
                            <xml>
                            <appid>{appid}</appid>
                            <body>{body}</body>
                            <mch_id>{mch_id}</mch_id>
                            <nonce_str>{nonce_str}</nonce_str>
                            <notify_url>{notify_url}</notify_url>
                            <out_trade_no>{out_trade_no}</out_trade_no>
                            <spbill_create_ip>{spbill_create_ip}</spbill_create_ip>
                            <total_fee>{total_fee}</total_fee>
                            <trade_type>{trade_type}</trade_type>
                            <scene_info>{scene_info}</scene_info>
                            <sign>{sign}</sign>
                            </xml>
                        """
        content = template.format(**data)
        headers = {'Content-Type': 'application/xml'}
        raw = requests.post(url, data=content, headers=headers)
        rdict = xml_response_to_dict(raw)
        print(rdict)
        return Response({})