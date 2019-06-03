import conf
import workers

from crons.tasks.utils import get_date_check
from db.models.activitylogs import ActivityLog
from db.models.notification import NotificationEvent
from options.registry.cleaning import (
    CLEANING_INTERVALS_ACTIVITY_LOGS,
    CLEANING_INTERVALS_NOTIFICATIONS
)
from polyaxon.settings import CronsCeleryTasks


@workers.app.task(name=CronsCeleryTasks.CLEAN_ACTIVITY_LOGS, ignore_result=True)
def clean_activity_logs() -> None:
    last_date = get_date_check(days=conf.get(CLEANING_INTERVALS_ACTIVITY_LOGS))
    ActivityLog.objects.filter(created_at__lte=last_date).delete()


@workers.app.task(name=CronsCeleryTasks.CLEAN_NOTIFICATIONS, ignore_result=True)
def clean_notifications() -> None:
    last_date = get_date_check(days=conf.get(CLEANING_INTERVALS_NOTIFICATIONS))
    NotificationEvent.objects.filter(created_at__lte=last_date).delete()
