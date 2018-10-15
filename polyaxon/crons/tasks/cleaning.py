from datetime import datetime, timedelta

from django.conf import settings

from db.models.activitylogs import ActivityLog
from db.models.notification import Notification
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CronsCeleryTasks


@celery_app.task(name=CronsCeleryTasks.CLEAN_ACTIVITY_LOGS, ignore_result=True)
def clean_activity_logs():
    last_date = datetime.today() - timedelta(days=settings.CleaningIntervals.ACTIVITY_LOGS)
    ActivityLog.objects.filter(created_at__lte=last_date).delete()


@celery_app.task(name=CronsCeleryTasks.CLEAN_NOTIFICATIONS, ignore_result=True)
def clean_notifications():
    last_date = datetime.today() - timedelta(days=settings.CleaningIntervals.NOTIFICATIONS)
    Notification.objects.filter(created_at__lte=last_date).delete()
