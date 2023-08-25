Configuration
=============

Configure your project using environment variables and settings.

Environment Variables
----------------------

| Variable Name | Description

| DJANGO_SETTINGS_MODULE  | Your settings module. `artists.settings.local` for local environment |
| SECRET_KEY              | Secret key for your Django project. Keep it secret! |
| DB_USER                 | Your database user `artists` for current docker-compose configuration |
| DB_PASS                 | Your database user password `artists` for current docker-compose configuration |
| DB_NAME                 | Your database name `artists` for current docker-compose configuration |
| DB_HOST                 | Your database host `postgres` for current docker-compose configuration |
| DB_PORT                 | Your database port `5432` for current docker-compose configuration |
| CELERY_RESULT_BACKEND   | URL for storing celery results, example `redis://redis:6379/0` |
| CELERY_BROKER_URL       | URL for celery broker, example `amqp://admin:password@rabbit:5672//?heartbeat=3600` |
| SENTRY_DSN              | DSN from your sentry account, which will be used for monitoring|

Settings
--------

Adjust your project settings in the `settings` module if needed. You can make a copy of
settings.local and use it in local environment

```python
# local.py

DEBUG = True  # Set to False for production

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = 'your-secret-key'

