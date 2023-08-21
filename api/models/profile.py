from django.db import models
from .abstract import WithCreatedUpdated, validate_phone_number, validate_url
from django.contrib.auth import get_user_model



User = get_user_model()


class Profile(WithCreatedUpdated):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=32, null=True, blank=True, validators=[validate_phone_number])
    avatar_url = models.CharField(max_length=256, null=True, blank=True, validators=[validate_url])

    def __str__(self):
        return f"Profile: {self.user.email} "


class UserTokenPassword(WithCreatedUpdated):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"User: {self.user.email} Token: {self.token}"

