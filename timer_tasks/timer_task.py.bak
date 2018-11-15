import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extract.settings')

timer_task = Celery('timer_tasks')
timer_task.config_from_object('django.conf:settings', namespace='CELERY')
timer_task.autodiscover_tasks()
