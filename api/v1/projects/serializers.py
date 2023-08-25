from django.contrib.auth.models import User
from api.models import Project, ProjectMedia
from rest_framework import serializers
from api.v1.users.serializers import UserSerializer, UserWithProfileSerializer


class ClientProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    client = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Project
        fields = ["id", "name", "description", "client"]


class GetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMedia
        fields = ["id", "name", "file"]


class GetClientProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    artist = UserWithProfileSerializer(read_only=True)
    media = GetMediaSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "artist", "media"]


class GetArtistProjectSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    client = UserWithProfileSerializer(read_only=True)
    media = GetMediaSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "client", "media"]


class ProjectMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMedia
        fields = "__all__"
