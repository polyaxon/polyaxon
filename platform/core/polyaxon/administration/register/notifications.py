from db.models.notification import Notification, NotificationEvent


def register(admin_register):
    admin_register(NotificationEvent)
    admin_register(Notification)
