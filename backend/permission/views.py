from django.contrib.auth.models import  User, update_last_login
from rest_framework import exceptions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RetrieveUserSerializer
from .throttles import LoginUserThrottle


class LoginView(ObtainAuthToken):
    throttle_classes = (LoginUserThrottle,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        except exceptions.ValidationError:
            raise ValueError('登录信息输入错误')
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        update_last_login(None, user)
        return Response({'token': token.key})


class UserInfoView(generics.RetrieveAPIView):
    """用户基本信息接口

    """
    serializer_class = RetrieveUserSerializer

    def get_object(self):
        self.request.user.profile.update_password_expired()
        return User.objects.get(id=self.request.user.id)


class UserLogoutView(APIView):
    """登出接口

    """

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=self.request.user).delete()
        return Response({})
