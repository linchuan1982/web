import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extract.settings')

timer_task = Celery('timer_tasks')
timer_task.config_from_object('timer_tasks.timer_config', namespace='CELERY')
