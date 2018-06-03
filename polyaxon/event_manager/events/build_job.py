from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

BUILD_JOB_STARTED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.STARTED)
BUILD_JOB_STARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.BUILD_JOB,
                                                event_actions.STARTED,
                                                event_subjects.TRIGGER)
BUILD_JOB_STOPPED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.STOPPED)
BUILD_JOB_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.BUILD_JOB,
                                                event_actions.STOPPED,
                                                event_subjects.TRIGGER)
BUILD_JOB_VIEWED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.VIEWED)
BUILD_JOB_NEW_STATUS = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.NEW_STATUS)
BUILD_JOB_FAILED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.FAILED)
BUILD_JOB_SUCCEEDED = '{}.{}'.format(event_subjects.BUILD_JOB, event_actions.SUCCEEDED)


class BuildJobStartedEvent(Event):
    event_type = BUILD_JOB_STARTED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class BuildJobStartedTriggeredEvent(Event):
    event_type = BUILD_JOB_STARTED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class BuildJobSoppedEvent(Event):
    event_type = BUILD_JOB_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class BuildJobSoppedTriggeredEvent(Event):
    event_type = BUILD_JOB_STOPPED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('target'),  # project, experiment_group, experiment
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class BuildJobViewedEvent(Event):
    event_type = BUILD_JOB_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class BuildJobNewStatusEvent(Event):
    event_type = BUILD_JOB_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('target'),  # project, experiment_group, experiment
    )


class BuildJobSucceededEvent(Event):
    event_type = BUILD_JOB_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('target'),  # project, experiment_group, experiment
    )


class BuildJobFailedEvent(Event):
    event_type = BUILD_JOB_FAILED
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('project.id'),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('target'),  # project, experiment_group, experiment
    )
