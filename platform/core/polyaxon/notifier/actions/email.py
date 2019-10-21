import notifier

from actions.registry.email import EmailAction

notifier.subscribe_action(EmailAction)
