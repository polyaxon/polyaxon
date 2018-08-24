from django.conf import settings

from action_manager.action import Action, logger
from action_manager.action_event import ActionExecutedEvent
from action_manager.utils.email import send_mass_template_mail
from event_manager.event_actions import EXECUTED
from event_manager.event_context import get_event_context, get_readable_event
from libs.string_utils import strip_spaces

EMAIL_ACTION_EXECUTED = 'email_action.{}'.format(EXECUTED)


class EmailActionExecutedEvent(ActionExecutedEvent):
    event_type = EMAIL_ACTION_EXECUTED


class EmailAction(Action):
    action_key = 'email'
    name = 'Email'
    event_type = EMAIL_ACTION_EXECUTED
    description = ("Send emails."
                   "Emails can be sent automatically "
                   "by subscribing to certain events on Polyaxon, "
                   "or manually triggered by a user operation.")

    @classmethod
    def _validate_config(cls, config):
        if not config:
            return {}

        recipients = config.get('recipients')
        if not recipients:
            return {}

        if isinstance(recipients, str):
            recipients = strip_spaces(recipients, sep=',', join=False)

        config['recipients'] = [email for email in recipients if email]
        return config

    @classmethod
    def _get_config(cls):
        return None

    @classmethod
    def serialize_event_to_context(cls, event):
        event_context = get_event_context(event)

        context = {
            'subject': event_context.subject_action,
            'notification': get_readable_event(event_context),
        }
        return {
            'subject_template': 'notifier/subject.txt',
            'body_template': 'notifier/body.txt',
            'context': context
        }

    @classmethod
    def _prepare(cls, context):
        context = context or {}
        context['subject_template'] = (
            context.get('subject_template') or
            context.get('subject') or
            ''
        )
        context['body_template'] = (
            context.get('body_template') or
            context.get('body') or
            ''
        )
        context['context'] = (
            context.get('context') or
            None
        )
        return context

    @classmethod
    def _execute(cls, data, config):
        if not all([settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD]):
            logger.debug("Email was not setup, skipping send.")
            return

        recipients = config.get('recipients')

        if not recipients:
            logger.warning("No emails given, skipping send.")
            return

        subject_template = data['subject_template']
        body_template = data['body_template']
        context = data['context']

        send_mass_template_mail(subject_template, body_template, recipients, context=context)
