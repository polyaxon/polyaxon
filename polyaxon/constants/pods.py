class EventTypes(object):
    ADDED = 'ADDED'
    MODIFIED = 'MODIFIED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'


class PodConditions(object):
    READY = 'Ready'
    INITIALIZED = 'Initialized'
    SCHEDULED = 'PodScheduled'

    VALUES = [READY, INITIALIZED, SCHEDULED]
