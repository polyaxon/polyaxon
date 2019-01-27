from typing import Dict

from hestia.string_utils import strip_spaces

import conf

from action_manager.action import Action, logger
from action_manager.action_event import ActionExecutedEvent
from action_manager.utils.email import send_mass_template_mail
from event_manager.event import Event
from event_manager.event_actions import EXECUTED
from event_manager.event_context import get_event_context, get_readable_event

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
    def _validate_config(cls, config: Dict) -> Dict:
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
    def _get_config(cls) -> None:
        return None

    @classmethod
    def serialize_event_to_context(cls, event: Event) -> Dict:
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
    def _prepare(cls, context: Dict):
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
    def _execute(cls, data: Dict, config: Dict) -> None:
        if not all([conf.get('EMAIL_HOST_USER'), conf.get('EMAIL_HOST_PASSWORD')]):
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
