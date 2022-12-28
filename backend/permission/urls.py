from django.urls import include, re_path
from common.routers import BaseRouter

from . import views, viewsets

router = BaseRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'groups', viewsets.GroupViewSet)
router.register(r'permissions', viewsets.PermissionViewSet, basename='permission')

urlpatterns = [
    re_path(r'users/login/?', views.LoginView.as_view()),
    re_path(r'users/logout/?', views.UserLogoutView.as_view()),
    re_path(r'users/info/?', views.UserInfoView.as_view()),
    re_path(r'^', include(router.urls))
]
