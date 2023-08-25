from django.contrib.auth.models import User
from api.models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Profile
        fields = ["id", "phone_number", "avatar_url", "user"]


class SlimProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "phone_number", "avatar_url"]


class GetProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "phone_number", "avatar_url", "user"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=128)


class TokenPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)


class UserWithProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    profile = SlimProfileSerializer(read_only=True, many=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile"]
