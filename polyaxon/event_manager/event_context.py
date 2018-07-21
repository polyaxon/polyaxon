def get_event_subject(event_type):
    """Return the first part of the event_type

    e.g.

    >>> Event.event_type = 'experiment.deleted'
    >>> Event.get_event_subject() == 'experiment'
    """
    return event_type.split('.')[0]


def get_event_action(event_type):
    """Return the second part of the event_type

    e.g.

    >>> Event.event_type = 'experiment.deleted'
    >>> Event.get_event_action() == 'deleted'
    """
    return event_type.split('.')[1]
