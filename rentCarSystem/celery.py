import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentCarSystem.settings')
app = Celery('rentCarSystem')
app.config_from_object('django.conf',namespace='CELERY')
app.autodiscover_tasks()

