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
    def test_events_subjects(self):
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
        assert experiment.ExperimentSucceededEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentFailedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResourcesViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentLogsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStatusesViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentJobsViewedEvent.get_event_subject() == 'experiment'

        # Experiment group
        assert experiment_group.ExperimentGroupCreatedEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupUpdatedEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupDeletedEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupViewedEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupStoppedEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupResumedEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupFinishedEvent.get_event_subject() == 'experiment_group'
        assert (experiment_group.ExperimentGroupExperimentsViewedEvent.get_event_subject() ==
                'experiment_group')
        assert experiment_group.ExperimentGroupIterationEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupRandomEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupGridEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupHyperbandEvent.get_event_subject() == 'experiment_group'
        assert experiment_group.ExperimentGroupBOEvent.get_event_subject() == 'experiment_group'

        # Experiment job
        assert experiment_job.ExperimentJobViewedEvent.get_event_subject() == 'experiment_job'
        assert experiment_job.ExperimentJobResourcesViewedEvent.get_event_subject() == 'experiment_job'
        assert experiment_job.ExperimentJobLogsViewedEvent.get_event_subject() == 'experiment_job'
        assert experiment_job.ExperimentJobStatusesViewedEvent.get_event_subject() == 'experiment_job'

        # Notebook
        assert notebook.NotebookStartedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookSoppedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookViewedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookNewStatusEvent.get_event_subject() == 'notebook'

        # Permission
        assert permission.PermissionProjectDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionRepoDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionExperimentGroupDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionExperimentDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionTensorboardDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionNotebookDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionExperimentJobDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionClusterDeniedEvent.get_event_subject() == 'permission'
        assert permission.PermissionUserRoleEvent.get_event_subject() == 'permission'

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

    def test_from_instance(self):
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
