from django.utils import timezone
from rest_framework.authentication import TokenAuthentication as TA
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings


class TokenAuthentication(TA):
    """"""

    def is_token_expired(self, token: Token):
        timedelta = timezone.now() - token.created
        return timedelta.total_seconds() > settings.AUTH_CONFIGS['TOKEN_EXPIRED']

    def authenticate_credentials(self, key: str):
        if not Token.objects.filter(key=key).exists():
            raise AuthenticationFailed('Invalid Token')

        token = Token.objects.get(key=key)

        if not token.user.is_active:
            raise AuthenticationFailed('Token user is not active')

        if self.is_token_expired(token):
            raise AuthenticationFailed('Token is already expired')

        token.created = timezone.now()
        token.save()
        return (token.user, token)
