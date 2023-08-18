from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, GetProfileSerializer, ChangePasswordSerializer
from api.models import Profile
from django.db.utils import IntegrityError
from rest_framework.validators import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserInfoViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ProfileViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ProfileSerializer
        return GetProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user__id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        # Add new data to the serializer's validated data
        new_data = {'user': self.request.user}
        serializer.validated_data.update(new_data)
        try:
            instance = serializer.save()
        except IntegrityError:
            raise ValidationError({"detail": "This user has profile already"})
        return instance


class ChangePasswordView(views.APIView):

    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type='object',
        properties={
            'old_password': openapi.Schema(type="string", description='Old password'),
            'new_password': openapi.Schema(type="string", description='New password'),
        }
    ))
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid()
        user = request.user
        if user.check_password(serializer.data['old_password']):
            user.set_password(serializer.data['new_password'])
            return Response({"message": "Password was changed successfully"}, status=status.HTTP_200_OK)
        else:
            raise ValidationError({"message": "Old password is not correct"})

