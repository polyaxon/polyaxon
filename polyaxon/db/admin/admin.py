from django.contrib.admin import site

from db.models.notification import NotificationEvent, Notification

site.register(NotificationEvent)
site.register(Notification)
