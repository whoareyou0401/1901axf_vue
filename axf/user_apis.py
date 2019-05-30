import uuid

from django.conf import settings
from django.core.cache import caches
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import RegisterSerializer
from .models import AxfUser

user_cache = caches['user']
class UserActionViewSet(ViewSet):
    # 注册
    @action(methods=["post"], detail=False)
    def register(self, request):
        if request.data.get("u_password") != request.data.get("u_password2"):
            return Response({"code": 1, "msg": "两次密码不一致"})
    #     先判断用户名是否可用
        serializer = RegisterSerializer(data=request.data)
    #     序列化器 实例化
        serializer.is_valid(raise_exception=True)
    #     判断序列化器的有效性
        user = AxfUser.create_user(dict(serializer.data))
        if user:
    #     还有校验
    #     创建用户加密密码
    #     返回结果
            return Response({"data": {"id": user.id}})
        else:
            return Response({"code": 2, "msg": "创建失败"})
    # 登录
    @action(methods=["post"], detail=False)
    def login(self, request):
        u_username = request.data.get("u_username")
        u_password = request.data.get("u_password")
        user = AxfUser.authenticate(u_username, u_password)
        if user:
            # 登录
            token = uuid.uuid4().hex
        #     设置缓存
            user_cache.set(token, user.pk, settings.USER_TOKEN_LIFE)
        #     返回结果
            return Response({"data": token})
        else:
            # 提示错误信息
            return Response({"msg": "用户名或密码错误", "code": 3})