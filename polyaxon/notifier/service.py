from django.core.exceptions import ObjectDoesNotExist

from action_manager.actions.email import EmailAction
from constants import user_system
from event_manager import event_subjects
from event_manager.event_service import EventService
from notifier.managers import default_action_manager, default_event_manager
from notifier.recipients import get_instance_and_project_recipients, get_project_recipients


class NotifierService(EventService):
    event_manager = default_event_manager
    action_manager = default_action_manager

    def __init__(self):
        self.notification_event = None
        self.notification = None

    @staticmethod
    def get_recipients(event: 'Event'):
        if event.get_event_subject() == event_subjects.PROJECT:
            return get_project_recipients(event.instance)
        return get_instance_and_project_recipients(event.instance)

    def create_notification(self, event, recipients):
        actor_id = event.data.get(event.actor_id)
        actor_id = actor_id if actor_id != user_system.USER_SYSTEM_ID else None
        notification_event = self.notification_event.objects.create(
            event_type=event.event_type,
            actor_id=actor_id if actor_id != user_system.USER_SYSTEM_ID else None,
            context=event.data,
            created_at=event.datetime,
            object_id=event.instance_id,
            content_type_id=event.instance_contenttype
        )

        self.notification.objects.bulk_create([
            self.notification(event=notification_event, user_id=recipient.id)
            for recipient in recipients
        ])

    @staticmethod
    def validate_event_instance(event):
        from django.contrib.contenttypes.models import ContentType

        instance_cond = (
            not event.instance and
            event.instance_id and
            event.instance_contenttype
        )

        if instance_cond:
            try:
                ct = ContentType.objects.get(id=event.instance_contenttype)
                instance = ct.get_object_for_this_type(id=event.instance_id)
                event.instance = instance
            except ObjectDoesNotExist:
                return None

        return event

    def record_event(self, event):
        event = self.validate_event_instance(event=event)
        if not event:  # No notification, reason is that the object is probably deleted from the db
            return

        recipients = self.get_recipients(event)
        self.create_notification(event, recipients)
        for action in self.action_manager.values:
            config = None
            if action == EmailAction:
                config = {'recipients': [r.email for r in recipients]}

            try:
                action.execute(context=event, config=config, from_user=None, from_event=True)
            except Exception as e:
                action.logger.warning('Action execution failed %s', e, exc_info=True)

    def setup(self) -> None:
        super().setup()
        # Load default event types and actions
        import notifier.actions  # noqa
        import notifier.events  # noqa

        from db.models.notification import NotificationEvent, Notification

        self.notification_event = NotificationEvent
        self.notification = Notification
