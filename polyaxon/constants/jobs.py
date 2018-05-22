from libs.constants import UNKNOWN
from libs.statuses import BaseStatuses


class JobLifeCycle(BaseStatuses):
    """Experiment lifecycle

    Props:
        * CREATED: created.
        * BUILDING: This includes time before being bound to a node,
                    as well as time spent pulling images onto the host.
        * RUNNING: The pod has been bound to a node and all of the containers have been started.
        * SUCCEEDED: All containers in the pod have voluntarily terminated with a
                     container exit code of 0, and the system is
                     not going to restart any of these containers.
        * FAILED: All containers in the pod have terminated,
                  and at least one container has terminated in a failure.
        * STOPPED: was stopped/deleted/killed
        * UNKNOWN: For some reason the state of the pod could not be obtained,
                   typically due to an error in communicating with the host of the pod.
    """
    CREATED = 'Created'
    BUILDING = 'Building'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    STOPPED = 'Stopped'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (BUILDING, BUILDING),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (STOPPED, STOPPED),
        (UNKNOWN, UNKNOWN),
    )

    STARTING_STATUS = {CREATED, BUILDING}
    RUNNING_STATUS = {BUILDING, RUNNING}
    DONE_STATUS = {FAILED, STOPPED, SUCCEEDED}
    FAILED_STATUS = {FAILED, }
