from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token


class YfExtractTokenMiddleware(MiddlewareMixin):
    """使用头部信息的token，将其转化成user对象"""

    def process_request(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is None:
            return
        token = header_token.replace('Token ', '')
        token_obj = Token.objects.filter(key=token).first()
        if token_obj is None:
            return
        request.user = token_obj.user
