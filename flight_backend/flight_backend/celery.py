from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight_backend.settings")

app = Celery("flight_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
       'fetch-other-data-hourly': {
        'task': 'api.tasks.as_flight_data', 
        'schedule': crontab(minute=0, hour='*/3'),
    },
}
