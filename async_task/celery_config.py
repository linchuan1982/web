import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extract.settings')

async_task = Celery('async_task')

async_task.config_from_object('async_task.task_config')
# async_task.conf.update(imports=('analysis.fetch', ))
# async_task.config_from_object('django.conf:settings')
# async_task.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

