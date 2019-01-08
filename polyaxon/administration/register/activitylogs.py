from administration.register.utils import ReadOnlyAdmin
from db.models.activitylogs import ActivityLog


class ActivityLogAdmin(ReadOnlyAdmin):
    pass


def register(admin_register):
    admin_register(ActivityLog, ActivityLogAdmin)
