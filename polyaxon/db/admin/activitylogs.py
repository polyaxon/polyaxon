from django.contrib.admin import site

from db.models.activitylogs import ActivityLog

site.register(ActivityLog)
