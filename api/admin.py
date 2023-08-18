from django.contrib import admin
from .models import Profile
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_first_name', "get_last_name", 'phone_number']

    @admin.display(ordering='user__username', description="Email/Username")
    def get_username(self, obj):
        return obj.user.username

    @admin.display(ordering='user__first_name', description="First Name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering='user__last_name', description="Last Name")
    def get_last_name(self, obj):
        return obj.user.last_name