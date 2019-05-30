from django.conf import settings
from django.db import models
import hashlib
# Create your models here.
class AxfUser(models.Model):
    u_username = models.CharField(
        max_length=30,
        verbose_name="用户名",
        unique=True,
        db_index=True
    )
    u_password = models.CharField(
        max_length=255,
        verbose_name="密码"
    )
    u_email = models.EmailField(
       verbose_name="邮箱"
    )

    @classmethod
    def make_password(cls, pwd):
        md5 = hashlib.md5()
        # md5.update((pwd+settings.SECRET_KEY).encode())
        md5.update((pwd).encode())
        return md5.hexdigest().upper()


    @classmethod
    def create_user(cls, data):
        if "u_password2" in data:
            data.pop("u_password2")
        # 去检查用户名
        if cls.objects.filter(u_username=data.get("u_username")).exists():
            return None
        # 对密码做加密
        data["u_password"] = cls.make_password(data.get("u_password"))
        return cls.objects.create(**data)

    @classmethod
    def authenticate(cls, username=None, password=None):
#         找人
        user = cls.objects.filter(
            u_username=username
        ).first()
#         校验密码
        if user and user.u_password == cls.make_password(password):
            return user

class BaseData(models.Model):
    img = models.CharField(
        max_length=255
    )
    name = models.CharField(
        max_length=80
    )
    trackid = models.CharField(
        max_length=20
    )
    class Meta:
        abstract = True

class Wheel(BaseData):

    class Meta:
        db_table = "axf_wheel"

class Nav(BaseData):

    class Meta:
        db_table = "axf_nav"

class MustBuy(BaseData):

    class Meta:
        db_table = "axf_mustbuy"

class Shop(BaseData):
    class Meta:
        db_table = "axf_shop"

class MainShow(BaseData):
    categoryid = models.CharField(
        max_length=255
    )
    brandname = models.CharField(
        max_length=255
    )
    img1 = models.CharField(
        max_length=255
    )
    childcid1 = models.CharField(
        max_length=255
    )
    productid1 = models.CharField(
        max_length=255
    )
    longname1 = models.CharField(
        max_length=255
    )
    price1 = models.CharField(
        max_length=255
    )
    marketprice1 = models.CharField(
        max_length=255
    )
    img2 = models.CharField(
        max_length=255
    )
    childcid2 = models.CharField(
        max_length=255
    )
    productid2 = models.CharField(
        max_length=255
    )
    longname2 = models.CharField(
        max_length=255
    )
    price2 = models.CharField(
        max_length=255
    )
    marketprice2 = models.CharField(
        max_length=255
    )

    img3 = models.CharField(
        max_length=255
    )
    childcid3 = models.CharField(
        max_length=255
    )
    productid3 = models.CharField(
        max_length=255
    )
    longname3 = models.CharField(
        max_length=255
    )
    price3 = models.CharField(
        max_length=255
    )
    marketprice3 = models.CharField(
        max_length=255
    )

class FoodTypes(models.Model):
    """typeid,typename,childtypenames,typesort)"""
    typeid = models.CharField(
        max_length=20
    )
    typename = models.CharField(
        max_length=255
    )
    childtypenames = models.CharField(
        max_length=255
    )
    typesort = models.IntegerField()

    class Meta:
        db_table = "axf_foodtypes"


class Goods(models.Model):
    productid = models.CharField(
        max_length=255
    )
    productimg = models.CharField(
        max_length=255
    )
    productname = models.CharField(
        max_length=255
    )
    productlongname = models.CharField(
        max_length=255
    )
    isxf = models.BooleanField(
        default=True
    )
    pmdesc = models.BooleanField(
        default=True
    )
    specifics = models.CharField(
        max_length=255
    )
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    marketprice = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    categoryid = models.IntegerField()
    childcid = models.IntegerField()
    childcidname = models.CharField(
        max_length=100
    )
    dealerid = models.CharField(
        max_length=30
    )
    storenums = models.IntegerField()

    productnum = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(
        AxfUser
    )
    c_goods = models.ForeignKey(
        Goods
    )
    c_goods_num = models.IntegerField(
        verbose_name="商品数量"
    )
    c_is_select = models.BooleanField(
        default=True
    )


class Order(models.Model):
    ORDER_STATUS = (
        (1, "待付款"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价")
    )
    number = models.CharField(
        max_length=255
    )
    user = models.ForeignKey(
        AxfUser
    )
    status = models.IntegerField(
        choices=ORDER_STATUS,
        verbose_name="订单状态"
    )
    is_select = models.BooleanField(
        default=True
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    pay_style = models.CharField(
        default="微信",
        max_length=30
    )

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="orderitems"
    )
    goods = models.ForeignKey(
        Goods
    )
    num = models.IntegerField()
    final_price = models.IntegerField()

