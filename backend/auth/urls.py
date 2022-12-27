from django.urls import include, re_path
from common.routers import YfRouter

from . import views, viewsets

router = YfRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'groups', viewsets.GroupViewSet)
router.register(r'permissions', viewsets.PermissionViewSet, basename='permission')

urlpatterns = [
    re_path(r'users/login/?', views.CustomObtainAuthTokenView.as_view()),
    re_path(r'users/logout/?', views.UserLogoutView.as_view()),
    re_path(r'users/info/?', views.UserInfoView.as_view()),
    re_path(r'groups/valid/?', views.GroupValidateView.as_view()),
    re_path(r'users/valid/?', views.UserValidateView.as_view()),
    re_path(r'^', include(router.urls))
]
