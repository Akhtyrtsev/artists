# Generated by Django 4.2.4 on 2023-08-18 09:29

import api.models.abstract
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar_url",
            field=models.CharField(
                blank=True,
                max_length=256,
                null=True,
                validators=[api.models.abstract.validate_url],
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=32,
                null=True,
                validators=[api.models.abstract.validate_phone_number],
            ),
        ),
    ]
