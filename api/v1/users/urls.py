from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from .views import (
    UserInfoViewSet,
    ProfileViewSet,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserInfoViewSet, basename="user")
router.register(r"profiles", ProfileViewSet, basename="profile")

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/change_password/", ChangePasswordView.as_view()),
    path("v1/reset_password/", PasswordResetRequestView.as_view()),
    path("v1/reset_password_confirm/", PasswordResetConfirmView.as_view()),
]
