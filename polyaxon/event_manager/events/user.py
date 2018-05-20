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


class UserRegisteredEvent(Event):
    event_type = USER_REGISTERED
    actor_id = 'id'
    attributes = (
        Attribute('id'),
    )


class UserUpdatedEvent(Event):
    event_type = USER_UPDATED
    actor_id = 'id'
    attributes = (
        Attribute('id'),
    )


class UserActivatedEvent(Event):
    event_type = USER_ACTIVATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('actor_id')
    )


class UserDeletedEvent(Event):
    event_type = USER_DELETED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('actor_id')
    )


class UserLDAPEvent(Event):
    event_type = USER_LDAP
    attributes = ()


class UserGITHUBEvent(Event):
    event_type = USER_GITHUB
    actor_id = 'id'
    attributes = (
        Attribute('id'),
    )


class UserGITLABEvent(Event):
    event_type = USER_GITLAB
    actor_id = 'id'
    attributes = (
        Attribute('id'),
    )


class UserBITBUCKETEvent(Event):
    event_type = USER_BITBUCKET
    actor_id = 'id'
    attributes = (
        Attribute('id'),
    )
