from libs.constants import UNKNOWN


class NodeLifeCycle(object):
    UNKNOWN = UNKNOWN
    READY = 'Ready'
    NOT_READY = 'NotReady'
    DELETED = 'Deleted'

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
