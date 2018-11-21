import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extract.settings')

timer_task = Celery('timer_task')
timer_task.config_from_object('timer_task.task_config', namespace='CELERY')
