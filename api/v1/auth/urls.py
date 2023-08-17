from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import UserRegistrationView
from django.urls import path, include

urlpatterns = [
    path('v1/token/', obtain_jwt_token),
    path('v1/token/refresh/', refresh_jwt_token),
    path('v1/token/verify/', verify_jwt_token),
    path('v1/registration/', UserRegistrationView.as_view())
]
