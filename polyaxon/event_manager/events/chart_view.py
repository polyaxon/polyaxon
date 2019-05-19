from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

CHART_VIEW_CREATED = '{}.{}'.format(event_subjects.CHART_VIEW,
                                    event_actions.CREATED)

CHART_VIEW_DELETED = '{}.{}'.format(event_subjects.CHART_VIEW,
                                    event_actions.DELETED)

EVENTS = {
    CHART_VIEW_CREATED,
    CHART_VIEW_DELETED
}


class ChartViewCreatedEvent(Event):
    event_type = CHART_VIEW_CREATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('experiment.id', is_required=False),
        Attribute('experiment.user.id', is_required=False),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
    )


class ChartViewDeletedEvent(Event):
    event_type = CHART_VIEW_DELETED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('experiment.id', is_required=False),
        Attribute('experiment.user.id', is_required=False),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
    )
