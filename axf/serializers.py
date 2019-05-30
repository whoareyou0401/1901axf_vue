from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.Serializer):

    u_username = serializers.CharField(
        max_length=20,
        min_length=3
    )
    u_password = serializers.CharField(
        max_length=10,
        min_length=5
    )
    u_password2 = serializers.CharField(
        max_length=10,
        min_length=5
    )
    u_email = serializers.EmailField()

    def validate(self, attrs):
        u_username = attrs.get("u_username")
        print(u_username, "validate被调用")
        return super().validate(attrs)


    # def create(self, validated_data):
    #     # 加密密码啊
    #     pwd = validated_data.get("u_password")
    #     validated_data["u_password"] = make_password(pwd)
    #     # validated_data.pop("u_password2")
    #     # delattr(self, "u_password2")
    #     data = {}
    #     data["u_username"] = validated_data.get("u_username")
    #     data["u_password"] = validated_data.get("u_password")
    #     data["u_email"] = validated_data.get("u_email")
    #     return AxfUser.objects.create(**data)

    def update(self, instance, validated_data):
        pass

class WheelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wheel
        fields = "__all__"


class NavSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = "__all__"


class MustBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = MustBuy
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"

class MainShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainShow
        fields = "__all__"

class FoodTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodTypes
        fields = ["typeid", "typename"]

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"

class CartGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ["productimg", "productlongname", "price"]

class CartItemSerializer(serializers.ModelSerializer):
    c_goods = CartGoodsSerializer()#序列化器
    class Meta:
        model = Cart
        fields = ["id", "c_goods", "c_is_select", "c_goods_num"]


class OrderItemSerializer(serializers.ModelSerializer):
    goods = CartGoodsSerializer()
    class Meta:
        model = OrderItem
        fields = ["goods", "num", "final_price"]

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["orderitems", "is_select", "number", "create_time"]