from rest_framework.throttling import SimpleRateThrottle


class LoginIpThrottle(SimpleRateThrottle):
    """
    登录功能通过IP限流
    """
    scope = 'login'

    def get_cache_key(self, request, view):
        # 通过ip限制节流
        return self.get_ident(request)


class LoginUserThrottle(SimpleRateThrottle):
    """
    登录功能通过用户id限流
    """
    scope = 'login'

    def get_cache_key(self, request, view):
        if 'username' in request.data:
            username = request.data['username']
        return username
