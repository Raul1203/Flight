from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flight_backend.settings")

app = Celery("flight_backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
