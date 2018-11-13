from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extract.settings')

async_app = Celery('extract')
async_app.config_from_object('django.conf:settings', namespace='CELERY')
async_app.autodiscover_tasks()
