from django.contrib import admin
from .models import Profile, Project, ProjectMedia, User
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db import models
from django import forms
from django.utils.html import format_html
from django.forms import Select

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["get_username", "get_first_name", "get_last_name", "phone_number"]

    @admin.display(ordering="user__username", description="Email/Username")
    def get_username(self, obj):
        return obj.user.username

    @admin.display(ordering="user__first_name", description="First Name")
    def get_first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering="user__last_name", description="Last Name")
    def get_last_name(self, obj):
        return obj.user.last_name


class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 3  # Number of empty book forms to display


class CustomForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    class Media:
        js = ("api/disable_add_button.js",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectMediaInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            # Define the condition for filtering the choices
            kwargs["queryset"] = (
                Group.objects.filter(name__icontains="client").last().user_set.all()
            )

        if db_field.name == "artist":
            # Define the condition for filtering the choices
            kwargs["queryset"] = (
                Group.objects.filter(name__icontains="artist").last().user_set.all()
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj, **kwargs)
        client_field = form.base_fields["client"]
        client_field.widget.can_add_related = False
        client_field.widget.can_change_related = False
        client_field.widget.can_delete_related = False
        artist_field = form.base_fields["artist"]
        artist_field.widget.can_add_related = False
        artist_field.widget.can_change_related = False
        artist_field.widget.can_delete_related = False
        return form
