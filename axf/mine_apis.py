from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Order
from .auth import LoginAuthentication

class UserInfoRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [LoginAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        # 查询该用户未付款和未收货的订单数量
        orders = Order.objects.filter(
            user=user, status__in=[1, 3]
        )
        # 查询未付款的订单数量
        not_pay_num = orders.filter(status=1).count()
        # 查询的未收货 可以使用减法计算得到
        not_send_num = orders.count() - not_pay_num

        result = {
            "user_info":{
                "u_username": user.u_username
            },
            "orders_not_pay_num": not_pay_num,
            "orders_not_send_num": not_send_num
        }
        return Response({"data": result})
