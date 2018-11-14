from django.contrib.admin import site

from db.admin.utils import ReadOnlyAdmin
from db.models.activitylogs import ActivityLog


class ActivityLogAdmin(ReadOnlyAdmin):
    pass


site.register(ActivityLog, ActivityLogAdmin)
