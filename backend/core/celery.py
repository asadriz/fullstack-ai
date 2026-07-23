from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# setting the Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()

# Register periodic tasks here as apps are added, e.g.:
# app.conf.beat_schedule = {
#     "my-task-every-hour": {
#         "task": "apps.my_app.tasks.my_task",
#         "schedule": crontab(minute=0),
#     },
# }
app.conf.beat_schedule = {}
