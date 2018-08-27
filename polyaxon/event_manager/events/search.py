from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

SEARCH_CREATED = '{}.{}'.format(event_subjects.SEARCH, event_actions.CREATED)


class SearchCreatedEvent(Event):
    event_type = SEARCH_CREATED
    actor = True
    actor_id = 'user.id'
    actor_name = 'user.username'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('content_type')
    )
