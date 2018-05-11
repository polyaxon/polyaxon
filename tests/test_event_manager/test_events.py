from event_manager.event import Attribute, Event
from event_manager.events import (
    cluster,
    experiment,
    experiment_group,
    experiment_job,
    notebook,
    permission,
    project,
    repo,
    superuser,
    tensorboard,
    user
)
from libs.json_utils import loads
from tests.utils import BaseTest


class TestEvents(BaseTest):
    def test_events_subjects(self):  # pylint:disable=too-many-statements
        # Cluster
        assert cluster.ClusterCreatedEvent.get_event_subject() == 'cluster'
        assert cluster.ClusterUpdatedEvent.get_event_subject() == 'cluster'
        assert cluster.ClusterNodeCreatedEvent.get_event_subject() == 'cluster_node'
        assert cluster.ClusterNodeUpdatedEvent.get_event_subject() == 'cluster_node'
        assert cluster.ClusterNodeDeletedEvent.get_event_subject() == 'cluster_node'
        assert cluster.ClusterNodeGPU.get_event_subject() == 'cluster_node'

        # Experiment
        assert experiment.ExperimentCreatedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentUpdatedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentDeletedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStoppedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResumedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentRestartedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentCopiedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentNewStatusEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentNewMetricEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentSucceededEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentFailedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResourcesViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentLogsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStatusesViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentJobsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentMetricsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentDeletedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStoppedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResumedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentRestartedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentCopiedTriggeredEvent.get_event_subject() == 'experiment'

        # Experiment group
        assert (experiment_group.ExperimentGroupCreatedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupUpdatedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupDeletedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupViewedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupStoppedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupResumedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupFinishedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupNewStatusEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupExperimentsViewedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupIterationEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupRandomEvent.get_event_subject() ==
                'experiment_group')
        assert experiment_group.ExperimentGroupGridEvent.get_event_subject() == 'experiment_group'
        assert (experiment_group.ExperimentGroupHyperbandEvent.get_event_subject() ==
                'experiment_group')
        assert experiment_group.ExperimentGroupBOEvent.get_event_subject() == 'experiment_group'
        assert (experiment_group.ExperimentGroupDeletedTriggeredEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupStoppedTriggeredEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupResumedTriggeredEvent.get_event_subject() ==
                'experiment_group')

        # Experiment job
        assert experiment_job.ExperimentJobViewedEvent.get_event_subject() == 'experiment_job'
        assert (experiment_job.ExperimentJobResourcesViewedEvent.get_event_subject() ==
                'experiment_job')
        assert experiment_job.ExperimentJobLogsViewedEvent.get_event_subject() == 'experiment_job'
        assert (experiment_job.ExperimentJobStatusesViewedEvent.get_event_subject() ==
                'experiment_job')

        # Notebook
        assert notebook.NotebookStartedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookSoppedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookViewedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookNewStatusEvent.get_event_subject() == 'notebook'

        # Permission
        assert permission.PermissionProjectDeniedEvent.get_event_subject() == 'project'
        assert permission.PermissionRepoDeniedEvent.get_event_subject() == 'repo'
        assert (permission.PermissionExperimentGroupDeniedEvent.get_event_subject() ==
                'experiment_group')
        assert permission.PermissionExperimentDeniedEvent.get_event_subject() == 'experiment'
        assert permission.PermissionTensorboardDeniedEvent.get_event_subject() == 'tensorboard'
        assert permission.PermissionNotebookDeniedEvent.get_event_subject() == 'notebook'
        assert permission.PermissionExperimentJobDeniedEvent.get_event_subject() == 'experiment_job'
        assert permission.PermissionClusterDeniedEvent.get_event_subject() == 'cluster'
        assert permission.PermissionUserRoleEvent.get_event_subject() == 'superuser'

        # Project
        assert project.ProjectCreatedEvent.get_event_subject() == 'project'
        assert project.ProjectUpdatedEvent.get_event_subject() == 'project'
        assert project.ProjectDeletedEvent.get_event_subject() == 'project'
        assert project.ProjectViewedEvent.get_event_subject() == 'project'
        assert project.ProjectSetPublicEvent.get_event_subject() == 'project'
        assert project.ProjectSetPrivateEvent.get_event_subject() == 'project'
        assert project.ProjectExperimentsViewedEvent.get_event_subject() == 'project'
        assert project.ProjectExperimentGroupsViewedEvent.get_event_subject() == 'project'

        # Repo
        assert repo.RepoCreatedEvent.get_event_subject() == 'repo'
        assert repo.RepoNewCommitEvent.get_event_subject() == 'repo'

        # Superuser
        assert superuser.SuperUserRoleGrantedEvent.get_event_subject() == 'superuser'
        assert superuser.SuperUserRoleRevokedEvent.get_event_subject() == 'superuser'

        # Tensorboard
        assert tensorboard.TensorboardStartedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardSoppedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardViewedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardNewStatusEvent.get_event_subject() == 'tensorboard'

        # User
        assert user.UserRegisteredEvent.get_event_subject() == 'user'
        assert user.UserUpdatedEvent.get_event_subject() == 'user'
        assert user.UserActivatedEvent.get_event_subject() == 'user'
        assert user.UserDeletedEvent.get_event_subject() == 'user'

    def test_events_actions(self):  # pylint:disable=too-many-statements
        # Cluster
        assert cluster.ClusterCreatedEvent.get_event_action() is None
        assert cluster.ClusterUpdatedEvent.get_event_action() is None
        assert cluster.ClusterNodeCreatedEvent.get_event_action() is None
        assert cluster.ClusterNodeUpdatedEvent.get_event_action() is None
        assert cluster.ClusterNodeDeletedEvent.get_event_action() is None
        assert cluster.ClusterNodeGPU.get_event_action() is None

        # Experiment
        assert experiment.ExperimentCreatedEvent.get_event_action() == 'created'
        assert experiment.ExperimentUpdatedEvent.get_event_action() == 'updated'
        assert experiment.ExperimentDeletedEvent.get_event_action() is None
        assert experiment.ExperimentViewedEvent.get_event_action() == 'viewed'
        assert experiment.ExperimentStoppedEvent.get_event_action() is None
        assert experiment.ExperimentResumedEvent.get_event_action() is None
        assert experiment.ExperimentRestartedEvent.get_event_action() is None
        assert experiment.ExperimentCopiedEvent.get_event_action() is None
        assert experiment.ExperimentNewStatusEvent.get_event_action() is None
        assert experiment.ExperimentNewMetricEvent.get_event_action() is None
        assert experiment.ExperimentSucceededEvent.get_event_action() is None
        assert experiment.ExperimentFailedEvent.get_event_action() is None
        assert experiment.ExperimentResourcesViewedEvent.get_event_action() == 'resources_viewed'
        assert experiment.ExperimentLogsViewedEvent.get_event_action() == 'logs_viewed'
        assert experiment.ExperimentStatusesViewedEvent.get_event_action() == 'statuses_viewed'
        assert experiment.ExperimentJobsViewedEvent.get_event_action() == 'jobs_viewed'
        assert experiment.ExperimentMetricsViewedEvent.get_event_action() == 'metrics_viewed'
        assert experiment.ExperimentDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert experiment.ExperimentStoppedTriggeredEvent.get_event_action() == 'stopped'
        assert experiment.ExperimentResumedTriggeredEvent.get_event_action() == 'resumed'
        assert experiment.ExperimentRestartedTriggeredEvent.get_event_action() == 'restarted'
        assert experiment.ExperimentCopiedTriggeredEvent.get_event_action() == 'copied'

        # Experiment group
        assert experiment_group.ExperimentGroupCreatedEvent.get_event_action() == 'created'
        assert experiment_group.ExperimentGroupUpdatedEvent.get_event_action() == 'updated'
        assert experiment_group.ExperimentGroupDeletedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupViewedEvent.get_event_action() == 'viewed'
        assert experiment_group.ExperimentGroupStoppedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupResumedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupFinishedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupNewStatusEvent.get_event_action() is None
        assert (experiment_group.ExperimentGroupExperimentsViewedEvent.get_event_action() ==
                'experiments_viewed')
        assert experiment_group.ExperimentGroupIterationEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupRandomEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupGridEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupHyperbandEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupBOEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert experiment_group.ExperimentGroupStoppedTriggeredEvent.get_event_action() == 'stopped'
        assert experiment_group.ExperimentGroupResumedTriggeredEvent.get_event_action() == 'resumed'

        # Experiment job
        assert experiment_job.ExperimentJobViewedEvent.get_event_action() == 'viewed'
        assert (experiment_job.ExperimentJobResourcesViewedEvent.get_event_action() ==
                'resources_viewed')
        assert experiment_job.ExperimentJobLogsViewedEvent.get_event_action() == 'logs_viewed'
        assert (experiment_job.ExperimentJobStatusesViewedEvent.get_event_action() ==
                'statuses_viewed')

        # Notebook
        assert notebook.NotebookStartedEvent.get_event_action() == 'started'
        assert notebook.NotebookSoppedEvent.get_event_action() == 'stopped'
        assert notebook.NotebookViewedEvent.get_event_action() == 'viewed'
        assert notebook.NotebookNewStatusEvent.get_event_action() is None

        # Permission
        assert permission.PermissionProjectDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionRepoDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionExperimentGroupDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionExperimentDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionTensorboardDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionNotebookDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionExperimentJobDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionClusterDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionUserRoleEvent.get_event_action() == 'denied'

        # Project
        assert project.ProjectCreatedEvent.get_event_action() == 'created'
        assert project.ProjectUpdatedEvent.get_event_action() == 'updated'
        assert project.ProjectDeletedEvent.get_event_action() == 'deleted'
        assert project.ProjectViewedEvent.get_event_action() == 'viewed'
        assert project.ProjectSetPublicEvent.get_event_action() == 'set_public'
        assert project.ProjectSetPrivateEvent.get_event_action() == 'set_private'
        assert project.ProjectExperimentsViewedEvent.get_event_action() == 'experiments_viewed'
        assert (project.ProjectExperimentGroupsViewedEvent.get_event_action() ==
                'experiment_groups_viewed')

        # Repo
        assert repo.RepoCreatedEvent.get_event_action() == 'created'
        assert repo.RepoNewCommitEvent.get_event_action() == 'new_commit'

        # Superuser
        assert superuser.SuperUserRoleGrantedEvent.get_event_action() == 'granted'
        assert superuser.SuperUserRoleRevokedEvent.get_event_action() == 'revoked'

        # Tensorboard
        assert tensorboard.TensorboardStartedEvent.get_event_action() == 'started'
        assert tensorboard.TensorboardSoppedEvent.get_event_action() == 'stopped'
        assert tensorboard.TensorboardViewedEvent.get_event_action() == 'viewed'
        assert tensorboard.TensorboardNewStatusEvent.get_event_action() is None

        # User
        assert user.UserRegisteredEvent.get_event_action() == 'registered'
        assert user.UserUpdatedEvent.get_event_action() == 'updated'
        assert user.UserActivatedEvent.get_event_action() == 'activated'
        assert user.UserDeletedEvent.get_event_action() == 'deleted'

    def test_serialize(self):
        class DummyEvent(Event):
            event_type = 'dummy.event'
            attributes = (
                Attribute('attr1'),
            )

        event = DummyEvent(attr1='test')
        event_serialized = event.serialize(dumps=False)
        assert event_serialized['type'] == 'dummy.event'
        assert event_serialized['uuid'] is not None
        assert event_serialized['timestamp'] is not None
        assert event_serialized['data']['attr1'] == 'test'

        event_serialized_dump = event.serialize()
        assert event_serialized == loads(event_serialized_dump)

    def test_get_value_from_instance(self):
        class DummyEvent(Event):
            event_type = 'dummy.event'

        class SimpleObject(object):
            attr1 = 'test'

        class ComposedObject(object):
            attr2 = SimpleObject()

        value = DummyEvent.get_value_from_instance(attr='attr1',
                                                   instance=SimpleObject())
        assert value == 'test'

        value = DummyEvent.get_value_from_instance(attr='attr2',
                                                   instance=SimpleObject())
        assert value is None

        value = DummyEvent.get_value_from_instance(attr='attr2.attr1',
                                                   instance=ComposedObject())
        assert value == 'test'

        value = DummyEvent.get_value_from_instance(attr='attr2.attr3',
                                                   instance=ComposedObject())
        assert value is None

        value = DummyEvent.get_value_from_instance(attr='attr2.attr1.attr3',
                                                   instance=ComposedObject())
        assert value is None

        value = DummyEvent.get_value_from_instance(attr='attr2.attr4.attr3',
                                                   instance=SimpleObject())
        assert value is None

    def test_from_instance_simple_event(self):
        class DummyEvent(Event):
            event_type = 'dummy.event'
            attributes = (
                Attribute('attr1'),
            )

        class DummyObject(object):
            attr1 = 'test'

        obj = DummyObject()
        event = DummyEvent.from_instance(obj)
        event_serialized = event.serialize(dumps=False)
        assert event_serialized['type'] == 'dummy.event'
        assert event_serialized['uuid'] is not None
        assert event_serialized['timestamp'] is not None
        assert event_serialized['data']['attr1'] == 'test'

    def test_from_instance_nested_event(self):
        class DummyEvent(Event):
            event_type = 'dummy.event'
            attributes = (
                Attribute('attr1'),
                Attribute('attr2.attr3'),
                Attribute('attr2.attr4', is_required=False),
            )

        class DummyObject(object):
            class NestedObject(object):
                attr3 = 'test2'

            attr1 = 'test'
            attr2 = NestedObject()

        obj = DummyObject()
        event = DummyEvent.from_instance(obj)
        event_serialized = event.serialize(dumps=False)
        assert event_serialized['type'] == 'dummy.event'
        assert event_serialized['uuid'] is not None
        assert event_serialized['timestamp'] is not None
        assert event_serialized['data']['attr1'] == 'test'
        assert event_serialized['data']['attr2.attr3'] == 'test2'
        assert event_serialized['data']['attr2.attr4'] is None

    def test_actor(self):
        class DummyEvent(Event):
            event_type = 'dummy.event'
            actor_id = 'actor_id'
            attributes = (
                Attribute('attr1'),
            )

        class DummyObject(object):
            attr1 = 'test'

        obj = DummyObject()
        with self.assertRaises(ValueError):
            DummyEvent.from_instance(obj)
