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

INSTALLED_APPS += [
    'silk',
]

MIDDLEWARE += [
    'django.middleware.common.CommonMiddleware',
    'silk.middleware.SilkyMiddleware',
]

SILKY_PYTHON_PROFILER = True  # Enable Python profiling
SILKY_PYTHON_PROFILER_BINARY = True  # Enable collection of binary profiles (requires 'py-spy' tool)

SILKY_INTERCEPT_PERCENT = 100  # Specify the percentage of requests to intercept (e.g., 100 means all requests)

SILKY_MAX_RECORDED_REQUESTS = 10  # Set the maximum number of recorded requests in the database

SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10  # Percentage of requests to check for exceeding the max recorded requests

SILKY_MAX_RECORDED_REQUESTS_AGE = 60 * 60  # Set the maximum age of recorded requests (in seconds)

SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, 'silk_profiles/')


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication'

    ),
}

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@example.com'  # Replace with your desired sender email
