import notifier

from action_manager.actions.email import EmailAction

notifier.subscribe_action(EmailAction)
