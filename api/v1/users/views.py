import datetime

from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, GetProfileSerializer, ChangePasswordSerializer, TokenPasswordSerializer, ResetPasswordSerializer
from api.tasks import send_email
from api.models import Profile, UserTokenPassword
from django.db.utils import IntegrityError
from rest_framework.validators import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from uuid import uuid4
from django.conf import settings
from django.utils import timezone


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


class PasswordResetRequestView(views.APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type='object',
        properties={
            'email': openapi.Schema(type="string", description='email'),
        }
    ))
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid()
        user = User.objects.filter(email=serializer.data['email']).last()
        if not user:
            raise ValidationError({"message": "User with this email doesn't exist"})

        token = str(uuid4())
        UserTokenPassword.objects.create(user=user, token=token)
        send_email.delay(subject="Password Reset", recipient_list=[user.email],
                         template_name="/app/api/templates/email_templates/password_reset_email.html",
                         context={"recipient_name": f"{user.first_name}",
                                  "link": f"{settings.FRONTEND_URL}?token={token}"})

        return Response({"message": "Reset Password Email was sent"})


class PasswordResetConfirmView(views.APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type='object',
        properties={
            'new_password': openapi.Schema(type="string", description='new_password'),
            'token': openapi.Schema(type="string", description='token'),
        }
    ))
    def post(self, request, *args, **kwargs):
        serializer = TokenPasswordSerializer(data=request.data)
        serializer.is_valid()
        user_token = UserTokenPassword.objects.filter(token=serializer.data['token'],
                                                      created__gt=timezone.now()-datetime.timedelta(hours=24),
                                                      is_valid=True).last()
        if not user_token:
            raise ValidationError({"message": "Reset password token is invalid or expired"})

        user = user_token.user
        user.set_password(serializer.data['new_password'])
        user.save()
        user_token.is_valid = False
        user_token.save()
        return Response({"message": "Password was reset"})

