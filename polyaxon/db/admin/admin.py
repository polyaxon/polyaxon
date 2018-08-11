from django.contrib.admin import site

from db.models.notification import Notification, NotificationEvent

site.register(NotificationEvent)
site.register(Notification)
