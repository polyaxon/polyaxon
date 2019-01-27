from crons.tasks.utils import get_date_check
from db.models.activitylogs import ActivityLog
from db.models.notification import NotificationEvent
from polyaxon.celery_api import celery_app
from polyaxon.settings import CleaningIntervals, CronsCeleryTasks


@celery_app.task(name=CronsCeleryTasks.CLEAN_ACTIVITY_LOGS, ignore_result=True)
def clean_activity_logs() -> None:
    last_date = get_date_check(days=CleaningIntervals.ACTIVITY_LOGS)
    ActivityLog.objects.filter(created_at__lte=last_date).delete()


@celery_app.task(name=CronsCeleryTasks.CLEAN_NOTIFICATIONS, ignore_result=True)
def clean_notifications() -> None:
    last_date = get_date_check(days=CleaningIntervals.NOTIFICATIONS)
    NotificationEvent.objects.filter(created_at__lte=last_date).delete()
