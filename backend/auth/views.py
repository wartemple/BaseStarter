from django.shortcuts import render
from captcha.views import CaptchaStore, captcha_image
from django.contrib.auth.models import Group, User, update_last_login
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.cache import never_cache
from rest_framework import exceptions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

