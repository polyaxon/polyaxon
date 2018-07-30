from action_manager.action import Action, logger
from action_manager.action_event import ActionExecutedEvent
from event_manager.event_actions import EXECUTED
from libs.mail import send_mass_template_mail

EMAIL_ACTION_EXECUTED = 'email_action.{}'.format(EXECUTED)


class EmailActionExecutedEvent(ActionExecutedEvent):
    event_type = EMAIL_ACTION_EXECUTED


class EmailAction(Action):
    key = 'email'
    name = 'Email'
    event_type = EMAIL_ACTION_EXECUTED
    description = ("Send emails."
                   "Emails can be sent automatically "
                   "by subscribing to certain events on Polyaxon, "
                   "or manually triggered by a user operation.")

    def _get_config(self):
        pass

    def _execute(self, data, config):
        recipients = [email for email in config.get('addresses', '').split(',') if email]

        if not recipients:
            logger.warning("No emails given. Skipping send.")

        subject_template = ''
        body_template = ''

        send_mass_template_mail(subject_template, body_template, {}, recipients)
