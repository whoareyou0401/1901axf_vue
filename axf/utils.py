from .models import *


def get_total_price(user_id):
    # 找用户选中的购物车数据
    cart_items = Cart.objects.filter(
        user_id=user_id,
        c_is_select=True
    ).select_related("c_goods")
    total_price = 0
    # 如果购物车内有选中的商品
    if cart_items.exists():
        # 如果有东西 计算总价
        for i in cart_items:
            total_price += (i.c_goods_num * i.c_goods.price)
    # 返回值是总价
    return total_price