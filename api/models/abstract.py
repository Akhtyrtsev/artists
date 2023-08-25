from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class WithCreatedUpdated(models.Model):
    """Provides and handles created date and updated date."""

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        abstract = True


def validate_phone_number(value):
    if (value is not None and value != "") and (
        not value.isdigit() or len(value) != 10
    ):
        raise ValidationError("Value must contain exactly 10 digits.")


def validate_url(value):
    validator = URLValidator()

    try:
        validator(value)
    except ValidationError as e:
        raise ValidationError("Invalid URL format.")
