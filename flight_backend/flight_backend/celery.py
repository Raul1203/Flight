from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight_backend.settings")

app = Celery("flight_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-flight-data-daily': {
        'task': 'api.tasks.fetch_and_store_flight_data', 
        'schedule': crontab(hour=0, minute=0),
    },
}
