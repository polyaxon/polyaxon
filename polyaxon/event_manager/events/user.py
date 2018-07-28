from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

USER_REGISTERED = '{}.{}'.format(event_subjects.USER, event_actions.REGISTERED)
USER_UPDATED = '{}.{}'.format(event_subjects.USER, event_actions.UPDATED)
USER_ACTIVATED = '{}.{}'.format(event_subjects.USER, event_actions.ACTIVATED)
USER_DELETED = '{}.{}'.format(event_subjects.USER, event_actions.DELETED)
USER_LDAP = '{}.{}'.format(event_subjects.USER, event_actions.LDAP)
USER_GITHUB = '{}.{}.{}'.format(event_subjects.USER, event_actions.AUTH, event_actions.GITHUB)
USER_GITLAB = '{}.{}.{}'.format(event_subjects.USER, event_actions.AUTH, event_actions.GITLAB)
USER_BITBUCKET = '{}.{}.{}'.format(event_subjects.USER, event_actions.AUTH, event_actions.BITBUCKET)
USER_AZURE = '{}.{}.{}'.format(event_subjects.USER, event_actions.AUTH, event_actions.AZURE)


class UserRegisteredEvent(Event):
    event_type = USER_REGISTERED
    actor = True
    actor_id = 'id'
    actor_name = 'username'


class UserUpdatedEvent(Event):
    event_type = USER_UPDATED
    actor = True
    actor_id = 'id'
    actor_name = 'username'


class UserActivatedEvent(Event):
    event_type = USER_ACTIVATED
    actor = True
    attributes = (
        Attribute('id'),
    )


class UserDeletedEvent(Event):
    event_type = USER_DELETED
    actor = True
    attributes = (
        Attribute('id'),
    )


class UserLDAPEvent(Event):
    event_type = USER_LDAP


class UserGITHUBEvent(Event):
    event_type = USER_GITHUB
    actor = True
    actor_id = 'id'
    actor_name = 'username'


class UserGITLABEvent(Event):
    event_type = USER_GITLAB
    actor = True
    actor_id = 'id'
    actor_name = 'username'


class UserBITBUCKETEvent(Event):
    event_type = USER_BITBUCKET
    actor = True
    actor_id = 'id'
    actor_name = 'username'


class UserAZUREEvent(Event):
    event_type = USER_AZURE
    actor = True
    actor_id = 'id'
    actor_name = 'username'
