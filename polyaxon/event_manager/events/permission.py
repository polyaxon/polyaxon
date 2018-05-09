from event_manager import event_actions, event_subjects
from event_manager.event import Attribute, Event

PERMISSION_PROJECT_DENIED = '{}.{}.{}'.format(event_subjects.PROJECT,
                                              event_actions.DENIED,
                                              event_subjects.PERMISSION)
PERMISSION_REPO_DENIED = '{}.{}.{}'.format(event_subjects.REPO,
                                           event_actions.DENIED,
                                           event_subjects.PERMISSION)
PERMISSION_EXPERIMENT_GROUP_DENIED = '{}.{}.{}'.format(event_subjects.EXPERIMENT_GROUP,
                                                       event_actions.DENIED,
                                                       event_subjects.PERMISSION)
PERMISSION_EXPERIMENT_DENIED = '{}.{}.{}'.format(event_subjects.EXPERIMENT,
                                                 event_actions.DENIED,
                                                 event_subjects.PERMISSION)
PERMISSION_TENSORBOARD_DENIED = '{}.{}.{}'.format(event_subjects.TENSORBOARD,
                                                  event_actions.DENIED,
                                                  event_subjects.PERMISSION)
PERMISSION_NOTEBOOK_DENIED = '{}.{}.{}'.format(event_subjects.NOTEBOOK,
                                               event_actions.DENIED,
                                               event_subjects.PERMISSION)
PERMISSION_EXPERIMENT_JOB_DENIED = '{}.{}.{}'.format(event_subjects.EXPERIMENT_JOB,
                                                     event_actions.DENIED,
                                                     event_subjects.PERMISSION)
PERMISSION_CLUSTER_DENIED = '{}.{}.{}'.format(event_subjects.CLUSTER,
                                              event_actions.DENIED,
                                              event_subjects.PERMISSION)
PERMISSION_USER_ROLE_DENIED = '{}.{}.{}'.format(event_subjects.SUPERUSER,
                                                event_actions.DENIED,
                                                event_subjects.PERMISSION)


class PermissionProjectDeniedEvent(Event):
    event_type = PERMISSION_PROJECT_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('id'),
        Attribute('user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionRepoDeniedEvent(Event):
    event_type = PERMISSION_REPO_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionExperimentGroupDeniedEvent(Event):
    event_type = PERMISSION_EXPERIMENT_GROUP_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionExperimentDeniedEvent(Event):
    event_type = PERMISSION_EXPERIMENT_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionTensorboardDeniedEvent(Event):
    event_type = PERMISSION_TENSORBOARD_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionNotebookDeniedEvent(Event):
    event_type = PERMISSION_NOTEBOOK_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionExperimentJobDeniedEvent(Event):
    event_type = PERMISSION_EXPERIMENT_JOB_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('project.id'),
        Attribute('project.user.id'),
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionClusterDeniedEvent(Event):
    event_type = PERMISSION_CLUSTER_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('actor_id'),
        Attribute('event')
    )


class PermissionUserRoleEvent(Event):
    event_type = PERMISSION_USER_ROLE_DENIED
    actor_id = 'actor_id'
    attributes = (
        Attribute('user_id'),
        Attribute('actor_id'),
        Attribute('event')
    )
