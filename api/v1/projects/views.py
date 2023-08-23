from rest_framework import viewsets, views, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import GetClientProjectSerializer, ClientProjectSerializer, GetArtistProjectSerializer, ProjectMediaSerializer
from api.models import Project, ProjectMedia
from django.db.utils import IntegrityError
from rest_framework.validators import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from uuid import uuid4
from django.conf import settings
from django.utils import timezone
from api.permissions import IsClient, IsArtist


class ClientProjectViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsClient)
    serializer_class = ClientProjectSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ClientProjectSerializer
        return GetClientProjectSerializer


    def get_queryset(self):
        return Project.objects.filter(client__id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Add new data to the serializer's validated data
        new_data = {'client': self.request.user}
        serializer.validated_data.update(new_data)
        try:
            instance = serializer.save()
        except IntegrityError:
            raise ValidationError({"detail": "Unable to save project"})
        return instance


class ArtistProjectViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = GetArtistProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(artist__id=self.request.user.id)


class CreateProjectMediaView(generics.CreateAPIView):
    queryset = ProjectMedia.objects.all()
    serializer_class = ProjectMediaSerializer
    permission_classes = (IsAuthenticated, IsClient)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.filter(client=request.user, id=serializer.validated_data['project'].id).exists()
        if not project:
            raise ValidationError({"message": "Cannot upload media. Unknown project"})
        instance = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)