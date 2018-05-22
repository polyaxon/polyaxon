from django.contrib.admin import site

from models.activitylogs import ActivityLog

site.register(ActivityLog)
