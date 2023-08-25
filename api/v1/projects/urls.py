from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import ClientProjectViewSet, ArtistProjectViewSet, CreateProjectMediaView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'projects'

router = DefaultRouter()
router.register(r'client-projects', ClientProjectViewSet, basename="client-project")
router.register(r'artist-projects', ArtistProjectViewSet, basename="artist-project")

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/upload-media', CreateProjectMediaView.as_view(), name="upload-media")
]
