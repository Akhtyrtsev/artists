from .base import *


ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME") or "artists",
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "USER": os.environ.get("DB_USER") or "root",
        "PASSWORD": os.environ.get("DB_PASS"),
        "TEST": {"NAME": "artsists_test"},
    },
}

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
RABBIT_USERNAME = os.environ.get("RABBIT_USERNAME")
RABBIT_PASSWORD = os.environ.get("RABBIT_USERNAME")
