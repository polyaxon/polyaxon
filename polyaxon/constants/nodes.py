from constants.unknown import UNKNOWN


class NodeLifeCycle(object):
    UNKNOWN = UNKNOWN
    READY = 'ready'
    NOT_READY = 'notReady'
    DELETED = 'deleted'

    CHOICES = (
        (UNKNOWN, UNKNOWN),
        (READY, READY),
        (NOT_READY, NOT_READY),
        (DELETED, DELETED)
    )


class NodeRoles(object):
    MASTER = 'master'
    AGENT = 'agent'

    CHOICES = (
        (MASTER, MASTER),
        (AGENT, AGENT)
    )
