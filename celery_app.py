import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_notifier.settings')

app = Celery('admin_notifier')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Для совместимости с from celery_app import shared_task
def shared_task(*args, **kwargs):
    from celery import shared_task as celery_shared_task
    return celery_shared_task(*args, **kwargs)
