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
EXPERIMENT_ARCHIVED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                     event_actions.ARCHIVED)
EXPERIMENT_RESTORED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                     event_actions.RESTORED)
EXPERIMENT_STOPPED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.STOPPED)
EXPERIMENT_RESUMED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                    event_actions.RESUMED)
EXPERIMENT_RESTARTED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                      event_actions.RESTARTED)
EXPERIMENT_COPIED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                   event_actions.COPIED)
EXPERIMENT_BOOKMARKED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                       event_actions.BOOKMARKED)
EXPERIMENT_UNBOOKMARKED = '{}.{}'.format(event_subjects.EXPERIMENT,
                                         event_actions.UNBOOKMARKED)
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
EXPERIMENT_CLEANED_TRIGGERED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.CLEANED,
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
    actor = True
    actor_id = 'user.id'
    actor_name = 'user.username'
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('created_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('is_resume', attr_type=bool),
        Attribute('is_restart', attr_type=bool),
        Attribute('is_copy', attr_type=bool),
        Attribute('is_clone', attr_type=bool),
        Attribute('is_independent', attr_type=bool),
        Attribute('has_specification', attr_type=bool),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentUpdatedEvent(Event):
    event_type = EXPERIMENT_UPDATED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
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
    actor = True
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


class ExperimentArchivedEvent(Event):
    event_type = EXPERIMENT_ARCHIVED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentRestoredEvent(Event):
    event_type = EXPERIMENT_RESTORED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentBookmarkedEvent(Event):
    event_type = EXPERIMENT_BOOKMARKED
    actor = True
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


class ExperimentUnBookmarkedEvent(Event):
    event_type = EXPERIMENT_UNBOOKMARKED
    actor = True
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
        Attribute('experiment_group.id', is_required=False)
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
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentLogsViewedEvent(Event):
    event_type = EXPERIMENT_LOGS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentOutputsDownloadedEvent(Event):
    event_type = EXPERIMENT_OUTPUTS_DOWNLOADED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentStatusesViewedEvent(Event):
    event_type = EXPERIMENT_STATUSES_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentJobsViewedEvent(Event):
    event_type = EXPERIMENT_JOBS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentMetricsViewedEvent(Event):
    event_type = EXPERIMENT_METRICS_VIEWED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('last_status'),
    )


class ExperimentDeletedTriggeredEvent(Event):
    event_type = EXPERIMENT_DELETED_TRIGGERED
    actor = True
    attributes = (
        Attribute('id'),
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('experiment_group.id', is_required=False),
        Attribute('experiment_group.user.id', is_required=False),
        Attribute('user.id'),
        Attribute('updated_at', is_datetime=True),
        Attribute('has_description', attr_type=bool),
        Attribute('last_status'),
        Attribute('framework', attr_type=bool, is_required=False),
    )


class ExperimentCleanedTriggeredEvent(Event):
    event_type = EXPERIMENT_CLEANED_TRIGGERED
    attributes = (
        Attribute('id'),
    )


class ExperimentStoppedTriggeredEvent(Event):
    event_type = EXPERIMENT_STOPPED_TRIGGERED
    actor = True
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


class ExperimentResumedTriggeredEvent(Event):
    event_type = EXPERIMENT_RESUMED_TRIGGERED
    actor = True
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


class ExperimentRestartedTriggeredEvent(Event):
    event_type = EXPERIMENT_RESTARTED_TRIGGERED
    actor = True
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


class ExperimentCopiedTriggeredEvent(Event):
    event_type = EXPERIMENT_COPIED_TRIGGERED
    actor = True
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
