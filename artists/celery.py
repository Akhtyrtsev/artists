from __future__ import absolute_import
import os
from celery import Celery
from statistics import mean
from celery.schedules import crontab
from django.conf import settings
import logging
import os


logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get("DJANGO_SETTINGS_MODULE"))

app = Celery('artists')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
