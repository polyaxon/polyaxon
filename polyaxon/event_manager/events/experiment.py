from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

EXPERIMENT_CREATED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.CREATED)
EXPERIMENT_UPDATED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.UPDATED)
EXPERIMENT_DELETED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.DELETED)
EXPERIMENT_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.VIEWED)
EXPERIMENT_STOPPED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.STOPPED)
EXPERIMENT_RESUMED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.RESUMED)
EXPERIMENT_RESTARTED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                      event_actions.RESTARTED)
EXPERIMENT_COPIED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.COPIED)
EXPERIMENT_NEW_STATUS = '{}.{}'.format(event_subjects.EXPERIMENT,
                                       event_actions.NEW_STATUS)
EXPERIMENT_NEW_METRIC = '{}.{}'.format(event_subjects.EXPERIMENT,
                                       event_actions.NEW_METRIC)
EXPERIMENT_SUCCEEDED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                      event_actions.SUCCEEDED)
EXPERIMENT_FAILED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.FAILED)
EXPERIMENT_DONE = '{}.{}'.format(event_subjects.EXPERIMENT,
                                 event_actions.DONE)
EXPERIMENT_RESOURCES_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                             event_actions.RESOURCES_VIEWED)
EXPERIMENT_LOGS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                        event_actions.LOGS_VIEWED)
EXPERIMENT_OUTPUTS_DOWNLOADED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                               event_actions.OUTPUTS_DOWNLOADED)
EXPERIMENT_STATUSES_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                            event_actions.STATUSES_VIEWED)
EXPERIMENT_JOBS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                        event_actions.JOBS_VIEWED)
EXPERIMENT_METRICS_VIEWED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                           event_actions.METRICS_VIEWED)
EXPERIMENT_DELETED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.DELETED,
                                                 event_subjects.TRIGGER)
EXPERIMENT_STOPPED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.STOPPED,
                                                 event_subjects.TRIGGER)
EXPERIMENT_RESUMED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.RESUMED,
                                                 event_subjects.TRIGGER)
EXPERIMENT_RESTARTED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                   event_actions.RESTARTED,
                                                   event_subjects.TRIGGER)
EXPERIMENT_COPIED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                event_actions.COPIED,
                                                event_subjects.TRIGGER)


class ExperimentCreatedEvent(Event):
    event_type = EXPERIMENT_CREATED
    actor_id = 'user.id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('is_copy', attr_type=bool),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentUpdatedEvent(Event):
    event_type = EXPERIMENT_UPDATED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentDeletedEvent(Event):
    event_type = EXPERIMENT_DELETED
    attributes = (
        Attribute('id'),
    )


class ExperimentViewedEvent(Event):
    event_type = EXPERIMENT_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentStoppedEvent(Event):
    event_type = EXPERIMENT_STOPPED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentResumedEvent(Event):
    event_type = EXPERIMENT_RESUMED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentRestartedEvent(Event):
    event_type = EXPERIMENT_RESTARTED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentCopiedEvent(Event):
    event_type = EXPERIMENT_COPIED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentNewStatusEvent(Event):
    event_type = EXPERIMENT_NEW_STATUS
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('last_status'),
        Attribute('previous_status', is_required=False),
    )


class ExperimentNewMetricEvent(Event):
    event_type = EXPERIMENT_NEW_METRIC
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('last_metric', attr_type=dict, is_required=False),
    )


class ExperimentSucceededEvent(Event):
    event_type = EXPERIMENT_SUCCEEDED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('previous_status', is_required=False),
    )


class ExperimentFailedEvent(Event):
    event_type = EXPERIMENT_FAILED
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('previous_status', is_required=False),
    )


class ExperimentDoneEvent(Event):
    event_type = EXPERIMENT_DONE
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('previous_status', is_required=False),
    )


class ExperimentResourcesViewedEvent(Event):
    event_type = EXPERIMENT_RESOURCES_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class ExperimentLogsViewedEvent(Event):
    event_type = EXPERIMENT_LOGS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class ExperimentOutputsDownloadedEvent(Event):
    event_type = EXPERIMENT_OUTPUTS_DOWNLOADED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class ExperimentStatusesViewedEvent(Event):
    event_type = EXPERIMENT_STATUSES_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class ExperimentJobsViewedEvent(Event):
    event_type = EXPERIMENT_JOBS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class ExperimentMetricsViewedEvent(Event):
    event_type = EXPERIMENT_METRICS_VIEWED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('last_status'),
    )


class ExperimentDeletedTriggeredEvent(Event):
    event_type = EXPERIMENT_DELETED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentStoppedTriggeredEvent(Event):
    event_type = EXPERIMENT_STOPPED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentResumedTriggeredEvent(Event):
    event_type = EXPERIMENT_RESUMED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentRestartedTriggeredEvent(Event):
    event_type = EXPERIMENT_RESTARTED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentCopiedTriggeredEvent(Event):
    event_type = EXPERIMENT_COPIED_TRIGGERED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )
