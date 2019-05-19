from uuid import uuid1

import pytest

from django.contrib.contenttypes.models import ContentType

from constants import user_system
from event_manager.event import Attribute, Event
from event_manager.events import (
    archive,
    bookmark,
    build_job,
    chart_view,
    cluster,
    experiment,
    experiment_group,
    experiment_job,
    job,
    notebook,
    operation,
    operation_run,
    permission,
    pipeline,
    pipeline_run,
    project,
    repo,
    search,
    superuser,
    tensorboard,
    user
)
from event_manager.events.experiment import ExperimentSucceededEvent
from factories.factory_experiments import ExperimentFactory
from libs.json_utils import loads
from tests.base.case import BaseTest


@pytest.mark.events_mark
class TestEvents(BaseTest):
    def test_events_subjects_clusters(self):
        assert cluster.ClusterCreatedEvent.get_event_subject() == 'cluster'
        assert cluster.ClusterUpdatedEvent.get_event_subject() == 'cluster'
        assert cluster.ClusterNodeCreatedEvent.get_event_subject() == 'cluster_node'
        assert cluster.ClusterNodeUpdatedEvent.get_event_subject() == 'cluster_node'
        assert cluster.ClusterNodeDeletedEvent.get_event_subject() == 'cluster_node'
        assert cluster.ClusterNodeGPU.get_event_subject() == 'cluster_node'

    def test_events_subjects_experiments(self):
        assert experiment.ExperimentCreatedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentUpdatedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentDeletedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentArchivedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentRestoredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentBookmarkedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentUnBookmarkedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStoppedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResumedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentRestartedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentCopiedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentNewStatusEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentNewMetricEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentSucceededEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentFailedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentDoneEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResourcesViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentLogsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentOutputsDownloadedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStatusesViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentJobsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentMetricsViewedEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentDeletedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentStoppedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentResumedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentCleanedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentRestartedTriggeredEvent.get_event_subject() == 'experiment'
        assert experiment.ExperimentCopiedTriggeredEvent.get_event_subject() == 'experiment'

    def test_events_subjects_groups(self):
        assert (experiment_group.ExperimentGroupCreatedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupUpdatedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupDeletedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupViewedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupArchivedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupRestoredEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupBookmarkedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupUnBookmarkedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupStoppedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupResumedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupSucceededEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupFailedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupDoneEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupNewStatusEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupExperimentsViewedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupStatusesViewedEvent.get_event_subject() ==
                'experiment_group')
        assert (experiment_group.ExperimentGroupMetricsViewedEvent.get_event_subject() ==
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

    def test_events_subjects_experiment_jobs(self):
        assert experiment_job.ExperimentJobViewedEvent.get_event_subject() == 'experiment_job'
        assert (experiment_job.ExperimentJobResourcesViewedEvent.get_event_subject() ==
                'experiment_job')
        assert experiment_job.ExperimentJobLogsViewedEvent.get_event_subject() == 'experiment_job'
        assert (experiment_job.ExperimentJobStatusesViewedEvent.get_event_subject() ==
                'experiment_job')
        assert (experiment_job.ExperimentJobNewStatusEvent.get_event_subject() ==
                'experiment_job')

    def test_events_subjects_notebooks(self):
        assert notebook.NotebookStartedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookStartedTriggeredEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookSoppedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookSoppedTriggeredEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookCleanedTriggeredEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookViewedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookNewStatusEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookFailedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookSucceededEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookUpdatedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookDeletedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookDeletedTriggeredEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookArchivedEvent.get_event_subject() == 'notebook'
        assert notebook.NotebookRestoredEvent.get_event_subject() == 'notebook'

    def test_events_subjects_jobs(self):
        assert job.JobCreatedEvent.get_event_subject() == 'job'
        assert job.JobUpdatedEvent.get_event_subject() == 'job'
        assert job.JobStartedEvent.get_event_subject() == 'job'
        assert job.JobStartedTriggeredEvent.get_event_subject() == 'job'
        assert job.JobSoppedEvent.get_event_subject() == 'job'
        assert job.JobSoppedTriggeredEvent.get_event_subject() == 'job'
        assert job.JobCleanedTriggeredEvent.get_event_subject() == 'job'
        assert job.JobViewedEvent.get_event_subject() == 'job'
        assert job.JobArchivedEvent.get_event_subject() == 'job'
        assert job.JobRestoredEvent.get_event_subject() == 'job'
        assert job.JobBookmarkedEvent.get_event_subject() == 'job'
        assert job.JobUnBookmarkedEvent.get_event_subject() == 'job'
        assert job.JobNewStatusEvent.get_event_subject() == 'job'
        assert job.JobFailedEvent.get_event_subject() == 'job'
        assert job.JobSucceededEvent.get_event_subject() == 'job'
        assert job.JobDoneEvent.get_event_subject() == 'job'
        assert job.JobDeletedEvent.get_event_subject() == 'job'
        assert job.JobDeletedTriggeredEvent.get_event_subject() == 'job'
        assert job.JobLogsViewedEvent.get_event_subject() == 'job'
        assert job.JobRestartedEvent.get_event_subject() == 'job'
        assert job.JobRestartedTriggeredEvent.get_event_subject() == 'job'
        assert job.JobStatusesViewedEvent.get_event_subject() == 'job'
        assert job.JobOutputsDownloadedEvent.get_event_subject() == 'job'

    def test_events_subjects_builds(self):
        assert build_job.BuildJobCreatedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobUpdatedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobStartedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobStartedTriggeredEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobSoppedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobSoppedTriggeredEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobCleanedTriggeredEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobViewedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobArchivedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobRestoredEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobBookmarkedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobUnBookmarkedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobNewStatusEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobFailedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobSucceededEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobDoneEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobDeletedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobDeletedTriggeredEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobLogsViewedEvent.get_event_subject() == 'build_job'
        assert build_job.BuildJobStatusesViewedEvent.get_event_subject() == 'build_job'

    def test_events_subjects_bookmarks(self):
        assert bookmark.BookmarkBuildJobsViewedEvent.get_event_subject() == 'bookmark'
        assert bookmark.BookmarkJobsViewedEvent.get_event_subject() == 'bookmark'
        assert bookmark.BookmarkExperimentsViewedEvent.get_event_subject() == 'bookmark'
        assert bookmark.BookmarkExperimentGroupsViewedEvent.get_event_subject() == 'bookmark'
        assert bookmark.BookmarkProjectsViewedEvent.get_event_subject() == 'bookmark'

    def test_events_subjects_archives(self):
        assert archive.ArchiveBuildJobsViewedEvent.get_event_subject() == 'archive'
        assert archive.ArchiveJobsViewedEvent.get_event_subject() == 'archive'
        assert archive.ArchiveExperimentsViewedEvent.get_event_subject() == 'archive'
        assert archive.ArchiveExperimentGroupsViewedEvent.get_event_subject() == 'archive'
        assert archive.ArchiveProjectsViewedEvent.get_event_subject() == 'archive'

    def test_events_subjects_searches(self):
        assert search.SearchCreatedEvent.get_event_subject() == 'search'
        assert search.SearchDeletedEvent.get_event_subject() == 'search'

    def test_events_subjects_chart_views(self):
        assert chart_view.ChartViewCreatedEvent.get_event_subject() == 'chart_view'
        assert chart_view.ChartViewDeletedEvent.get_event_subject() == 'chart_view'

    def test_events_subjects_permissions(self):
        assert permission.PermissionProjectDeniedEvent.get_event_subject() == 'project'
        assert permission.PermissionRepoDeniedEvent.get_event_subject() == 'repo'
        assert (permission.PermissionExperimentGroupDeniedEvent.get_event_subject() ==
                'experiment_group')
        assert permission.PermissionExperimentDeniedEvent.get_event_subject() == 'experiment'
        assert permission.PermissionTensorboardDeniedEvent.get_event_subject() == 'tensorboard'
        assert permission.PermissionNotebookDeniedEvent.get_event_subject() == 'notebook'
        assert permission.PermissionBuildJobDeniedEvent.get_event_subject() == 'build_job'
        assert permission.PermissionExperimentJobDeniedEvent.get_event_subject() == 'experiment_job'
        assert permission.PermissionClusterDeniedEvent.get_event_subject() == 'cluster'
        assert permission.PermissionUserRoleEvent.get_event_subject() == 'superuser'

    def test_events_subjects_projects(self):
        assert project.ProjectCreatedEvent.get_event_subject() == 'project'
        assert project.ProjectUpdatedEvent.get_event_subject() == 'project'
        assert project.ProjectDeletedEvent.get_event_subject() == 'project'
        assert project.ProjectDeletedTriggeredEvent.get_event_subject() == 'project'
        assert project.ProjectViewedEvent.get_event_subject() == 'project'
        assert project.ProjectArchivedEvent.get_event_subject() == 'project'
        assert project.ProjectRestoredEvent.get_event_subject() == 'project'
        assert project.ProjectBookmarkedEvent.get_event_subject() == 'project'
        assert project.ProjectUnBookmarkedEvent.get_event_subject() == 'project'
        assert project.ProjectSetPublicEvent.get_event_subject() == 'project'
        assert project.ProjectSetPrivateEvent.get_event_subject() == 'project'
        assert project.ProjectExperimentsViewedEvent.get_event_subject() == 'project'
        assert project.ProjectExperimentGroupsViewedEvent.get_event_subject() == 'project'
        assert project.ProjectJobsViewedEvent.get_event_subject() == 'project'
        assert project.ProjectBuildsViewedEvent.get_event_subject() == 'project'
        assert project.ProjectTensorboardsViewedEvent.get_event_subject() == 'project'
        assert project.ProjectNotebooksViewedEvent.get_event_subject() == 'project'

    def test_events_subjects_repos(self):
        assert repo.RepoCreatedEvent.get_event_subject() == 'repo'
        assert repo.RepoNewCommitEvent.get_event_subject() == 'repo'

    def test_events_subjects_superusers(self):
        assert superuser.SuperUserRoleGrantedEvent.get_event_subject() == 'superuser'
        assert superuser.SuperUserRoleRevokedEvent.get_event_subject() == 'superuser'

    def test_events_subjects_tensorboards(self):
        assert tensorboard.TensorboardStartedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardStartedTriggeredEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardSoppedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardSoppedTriggeredEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardCleanedTriggeredEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardViewedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardBookmarkedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardUnBookmarkedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardNewStatusEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardFailedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardSucceededEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardStatusesViewedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardUpdatedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardDeletedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardDeletedTriggeredEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardArchivedEvent.get_event_subject() == 'tensorboard'
        assert tensorboard.TensorboardRestoredEvent.get_event_subject() == 'tensorboard'

    def test_events_subjects_users(self):
        assert user.UserRegisteredEvent.get_event_subject() == 'user'
        assert user.UserUpdatedEvent.get_event_subject() == 'user'
        assert user.UserActivatedEvent.get_event_subject() == 'user'
        assert user.UserDeletedEvent.get_event_subject() == 'user'
        assert user.UserLDAPEvent.get_event_subject() == 'user'
        assert user.UserGITHUBEvent.get_event_subject() == 'user'
        assert user.UserGITLABEvent.get_event_subject() == 'user'
        assert user.UserBITBUCKETEvent.get_event_subject() == 'user'
        assert user.UserAZUREEvent.get_event_subject() == 'user'

    def test_events_subjects_pipelines(self):
        assert pipeline.PipelineCreatedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineUpdatedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineDeletedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineViewedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineArchivedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineRestoredEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineBookmarkedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineUnbookmarkedEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineDeletedTriggeredEvent.get_event_subject() == 'pipeline'
        assert pipeline.PipelineCleanedTriggeredEvent.get_event_subject() == 'pipeline'

    def test_events_subjects_operations(self):
        assert operation.OperationCreatedEvent.get_event_subject() == 'operation'
        assert operation.OperationUpdatedEvent.get_event_subject() == 'operation'
        assert operation.OperationDeletedEvent.get_event_subject() == 'operation'
        assert operation.OperationViewedEvent.get_event_subject() == 'operation'
        assert operation.OperationArchivedEvent.get_event_subject() == 'operation'
        assert operation.OperationRestoredEvent.get_event_subject() == 'operation'
        assert operation.OperationDeletedTriggeredEvent.get_event_subject() == 'operation'
        assert operation.OperationCleanedTriggeredEvent.get_event_subject() == 'operation'

    def test_events_subjects_pipeline_runs(self):
        assert pipeline_run.PipelineRunCreatedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunUpdatedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunDeletedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunViewedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunArchivedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunRestoredEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunStoppedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunSkippedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunResumedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunRestartedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunNewStatusEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunSucceededEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunFailedEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunDoneEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunDeletedTriggeredEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunCleanedTriggeredEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunStoppedTriggeredEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunResumedTriggeredEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunRestartedTriggeredEvent.get_event_subject() == 'pipeline_run'
        assert pipeline_run.PipelineRunSkippedTriggeredEvent.get_event_subject() == 'pipeline_run'

    def test_events_subjects_operation_runs(self):
        assert operation_run.OperationRunCreatedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunUpdatedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunDeletedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunViewedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunArchivedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunRestoredEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunStoppedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunSkippedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunResumedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunRestartedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunNewStatusEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunSucceededEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunFailedEvent.get_event_subject() == 'operation_run'
        assert operation_run.OperationRunDoneEvent.get_event_subject() == 'operation_run'
        assert (operation_run.OperationRunDeletedTriggeredEvent.get_event_subject() ==
                'operation_run')
        assert (operation_run.OperationRunCleanedTriggeredEvent.get_event_subject() ==
                'operation_run')
        assert (operation_run.OperationRunStoppedTriggeredEvent.get_event_subject() ==
                'operation_run')
        assert (operation_run.OperationRunResumedTriggeredEvent.get_event_subject() ==
                'operation_run')
        assert (operation_run.OperationRunRestartedTriggeredEvent.get_event_subject() ==
                'operation_run')
        assert (operation_run.OperationRunSkippedTriggeredEvent.get_event_subject() ==
                'operation_run')

    def test_events_actions_clusters(self):
        assert cluster.ClusterCreatedEvent.get_event_action() is None
        assert cluster.ClusterUpdatedEvent.get_event_action() is None
        assert cluster.ClusterNodeCreatedEvent.get_event_action() is None
        assert cluster.ClusterNodeUpdatedEvent.get_event_action() is None
        assert cluster.ClusterNodeDeletedEvent.get_event_action() is None
        assert cluster.ClusterNodeGPU.get_event_action() is None

    def test_events_actions_experiments(self):
        assert experiment.ExperimentCreatedEvent.get_event_action() == 'created'
        assert experiment.ExperimentUpdatedEvent.get_event_action() == 'updated'
        assert experiment.ExperimentDeletedEvent.get_event_action() is None
        assert experiment.ExperimentViewedEvent.get_event_action() == 'viewed'
        assert experiment.ExperimentArchivedEvent.get_event_action() == 'archived'
        assert experiment.ExperimentRestoredEvent.get_event_action() == 'restored'
        assert experiment.ExperimentBookmarkedEvent.get_event_action() == 'bookmarked'
        assert experiment.ExperimentUnBookmarkedEvent.get_event_action() == 'unbookmarked'
        assert experiment.ExperimentStoppedEvent.get_event_action() is None
        assert experiment.ExperimentResumedEvent.get_event_action() is None
        assert experiment.ExperimentRestartedEvent.get_event_action() is None
        assert experiment.ExperimentCopiedEvent.get_event_action() is None
        assert experiment.ExperimentNewStatusEvent.get_event_action() is None
        assert experiment.ExperimentNewMetricEvent.get_event_action() is None
        assert experiment.ExperimentSucceededEvent.get_event_action() is None
        assert experiment.ExperimentFailedEvent.get_event_action() is None
        assert experiment.ExperimentDoneEvent.get_event_action() is None
        assert experiment.ExperimentResourcesViewedEvent.get_event_action() == 'resources_viewed'
        assert experiment.ExperimentLogsViewedEvent.get_event_action() == 'logs_viewed'
        assert (experiment.ExperimentOutputsDownloadedEvent.get_event_action() ==
                'outputs_downloaded')
        assert experiment.ExperimentStatusesViewedEvent.get_event_action() == 'statuses_viewed'
        assert experiment.ExperimentJobsViewedEvent.get_event_action() == 'jobs_viewed'
        assert experiment.ExperimentMetricsViewedEvent.get_event_action() == 'metrics_viewed'
        assert experiment.ExperimentCleanedTriggeredEvent.get_event_action() is None
        assert experiment.ExperimentDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert experiment.ExperimentStoppedTriggeredEvent.get_event_action() == 'stopped'
        assert experiment.ExperimentResumedTriggeredEvent.get_event_action() == 'resumed'
        assert experiment.ExperimentRestartedTriggeredEvent.get_event_action() == 'restarted'
        assert experiment.ExperimentCopiedTriggeredEvent.get_event_action() == 'copied'

    def test_events_actions_groups(self):
        assert experiment_group.ExperimentGroupCreatedEvent.get_event_action() == 'created'
        assert experiment_group.ExperimentGroupUpdatedEvent.get_event_action() == 'updated'
        assert experiment_group.ExperimentGroupDeletedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupViewedEvent.get_event_action() == 'viewed'
        assert experiment_group.ExperimentGroupArchivedEvent.get_event_action() == 'archived'
        assert experiment_group.ExperimentGroupRestoredEvent.get_event_action() == 'restored'
        assert experiment_group.ExperimentGroupBookmarkedEvent.get_event_action() == 'bookmarked'
        assert (experiment_group.ExperimentGroupUnBookmarkedEvent.get_event_action() ==
                'unbookmarked')
        assert experiment_group.ExperimentGroupStoppedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupResumedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupSucceededEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupFailedEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupDoneEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupNewStatusEvent.get_event_action() is None
        assert (experiment_group.ExperimentGroupExperimentsViewedEvent.get_event_action() ==
                'experiments_viewed')
        assert (experiment_group.ExperimentGroupStatusesViewedEvent.get_event_action() ==
                'statuses_viewed')
        assert (experiment_group.ExperimentGroupMetricsViewedEvent.get_event_action() ==
                'metrics_viewed')
        assert experiment_group.ExperimentGroupIterationEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupRandomEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupGridEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupHyperbandEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupBOEvent.get_event_action() is None
        assert experiment_group.ExperimentGroupDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert experiment_group.ExperimentGroupStoppedTriggeredEvent.get_event_action() == 'stopped'
        assert experiment_group.ExperimentGroupResumedTriggeredEvent.get_event_action() == 'resumed'

    def test_events_actions_experiment_jobs(self):
        assert experiment_job.ExperimentJobViewedEvent.get_event_action() == 'viewed'
        assert (experiment_job.ExperimentJobResourcesViewedEvent.get_event_action() ==
                'resources_viewed')
        assert experiment_job.ExperimentJobLogsViewedEvent.get_event_action() == 'logs_viewed'
        assert (experiment_job.ExperimentJobStatusesViewedEvent.get_event_action() ==
                'statuses_viewed')
        assert experiment_job.ExperimentJobNewStatusEvent.get_event_action() is None

    def test_events_actions_notebooks(self):
        assert notebook.NotebookStartedEvent.get_event_action() is None
        assert notebook.NotebookStartedTriggeredEvent.get_event_action() == 'started'
        assert notebook.NotebookSoppedEvent.get_event_action() is None
        assert notebook.NotebookSoppedTriggeredEvent.get_event_action() == 'stopped'
        assert notebook.NotebookCleanedTriggeredEvent.get_event_action() is None
        assert notebook.NotebookViewedEvent.get_event_action() == 'viewed'
        assert notebook.NotebookNewStatusEvent.get_event_action() is None
        assert notebook.NotebookFailedEvent.get_event_action() is None
        assert notebook.NotebookSucceededEvent.get_event_action() is None
        assert notebook.NotebookStatusesViewedEvent.get_event_action() == 'statuses_viewed'
        assert notebook.NotebookUpdatedEvent.get_event_action() == 'updated'
        assert notebook.NotebookDeletedEvent.get_event_action() is None
        assert notebook.NotebookDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert notebook.NotebookArchivedEvent.get_event_action() == 'archived'
        assert notebook.NotebookRestoredEvent.get_event_action() == 'restored'

    def test_events_actions_jobs(self):
        assert job.JobCreatedEvent.get_event_action() == 'created'
        assert job.JobUpdatedEvent.get_event_action() == 'updated'
        assert job.JobStartedEvent.get_event_action() is None
        assert job.JobStartedTriggeredEvent.get_event_action() == 'started'
        assert job.JobSoppedEvent.get_event_action() is None
        assert job.JobSoppedTriggeredEvent.get_event_action() == 'stopped'
        assert job.JobCleanedTriggeredEvent.get_event_action() is None
        assert job.JobViewedEvent.get_event_action() == 'viewed'
        assert job.JobBookmarkedEvent.get_event_action() == 'bookmarked'
        assert job.JobUnBookmarkedEvent.get_event_action() == 'unbookmarked'
        assert job.JobNewStatusEvent.get_event_action() is None
        assert job.JobFailedEvent.get_event_action() is None
        assert job.JobSucceededEvent.get_event_action() is None
        assert job.JobDoneEvent.get_event_action() is None
        assert job.JobDeletedEvent.get_event_action() is None
        assert job.JobDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert job.JobLogsViewedEvent.get_event_action() == 'logs_viewed'
        assert job.JobRestartedEvent.get_event_action() is None
        assert job.JobRestartedTriggeredEvent.get_event_action() == 'restarted'
        assert job.JobStatusesViewedEvent.get_event_action() == 'statuses_viewed'
        assert job.JobOutputsDownloadedEvent.get_event_action() == 'outputs_downloaded'

    def test_events_actions_builds(self):
        assert build_job.BuildJobCreatedEvent.get_event_action() == 'created'
        assert build_job.BuildJobUpdatedEvent.get_event_action() == 'updated'
        assert build_job.BuildJobStartedEvent.get_event_action() is None
        assert build_job.BuildJobStartedTriggeredEvent.get_event_action() == 'started'
        assert build_job.BuildJobSoppedEvent.get_event_action() is None
        assert build_job.BuildJobSoppedTriggeredEvent.get_event_action() == 'stopped'
        assert build_job.BuildJobCleanedTriggeredEvent.get_event_action() is None
        assert build_job.BuildJobViewedEvent.get_event_action() == 'viewed'
        assert build_job.BuildJobArchivedEvent.get_event_action() == 'archived'
        assert build_job.BuildJobRestoredEvent.get_event_action() == 'restored'
        assert build_job.BuildJobBookmarkedEvent.get_event_action() == 'bookmarked'
        assert build_job.BuildJobUnBookmarkedEvent.get_event_action() == 'unbookmarked'
        assert build_job.BuildJobNewStatusEvent.get_event_action() is None
        assert build_job.BuildJobFailedEvent.get_event_action() is None
        assert build_job.BuildJobSucceededEvent.get_event_action() is None
        assert build_job.BuildJobDoneEvent.get_event_action() is None
        assert build_job.BuildJobDeletedEvent.get_event_action() is None
        assert build_job.BuildJobDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert build_job.BuildJobLogsViewedEvent.get_event_action() == 'logs_viewed'
        assert build_job.BuildJobStatusesViewedEvent.get_event_action() == 'statuses_viewed'

    def test_events_actions_bookmarks(self):
        assert bookmark.BookmarkBuildJobsViewedEvent.get_event_action() == 'builds_viewed'
        assert bookmark.BookmarkJobsViewedEvent.get_event_action() == 'jobs_viewed'
        assert bookmark.BookmarkExperimentsViewedEvent.get_event_action() == 'experiments_viewed'
        assert (bookmark.BookmarkExperimentGroupsViewedEvent.get_event_action() ==
                'experiment_groups_viewed')
        assert bookmark.BookmarkProjectsViewedEvent.get_event_action() == 'projects_viewed'

    def test_events_actions_archive(self):
        assert archive.ArchiveBuildJobsViewedEvent.get_event_action() == 'builds_viewed'
        assert archive.ArchiveJobsViewedEvent.get_event_action() == 'jobs_viewed'
        assert archive.ArchiveExperimentsViewedEvent.get_event_action() == 'experiments_viewed'
        assert (archive.ArchiveExperimentGroupsViewedEvent.get_event_action() ==
                'experiment_groups_viewed')
        assert archive.ArchiveProjectsViewedEvent.get_event_action() == 'projects_viewed'

    def test_events_actions_searches(self):
        assert search.SearchCreatedEvent.get_event_action() == 'created'
        assert search.SearchDeletedEvent.get_event_action() == 'deleted'

    def test_events_actions_chart_views(self):
        assert chart_view.ChartViewCreatedEvent.get_event_action() == 'created'
        assert chart_view.ChartViewDeletedEvent.get_event_action() == 'deleted'

    def test_events_actions_permissions(self):
        assert permission.PermissionProjectDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionRepoDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionExperimentGroupDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionExperimentDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionTensorboardDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionNotebookDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionBuildJobDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionExperimentJobDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionClusterDeniedEvent.get_event_action() == 'denied'
        assert permission.PermissionUserRoleEvent.get_event_action() == 'denied'

    def test_events_actions_projects(self):
        assert project.ProjectCreatedEvent.get_event_action() == 'created'
        assert project.ProjectUpdatedEvent.get_event_action() == 'updated'
        assert project.ProjectDeletedEvent.get_event_action() is None
        assert project.ProjectDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert project.ProjectViewedEvent.get_event_action() == 'viewed'
        assert project.ProjectArchivedEvent.get_event_action() == 'archived'
        assert project.ProjectRestoredEvent.get_event_action() == 'restored'
        assert project.ProjectBookmarkedEvent.get_event_action() == 'bookmarked'
        assert project.ProjectUnBookmarkedEvent.get_event_action() == 'unbookmarked'
        assert project.ProjectSetPublicEvent.get_event_action() is None
        assert project.ProjectSetPrivateEvent.get_event_action() is None
        assert project.ProjectExperimentsViewedEvent.get_event_action() == 'experiments_viewed'
        assert (project.ProjectExperimentGroupsViewedEvent.get_event_action() ==
                'experiment_groups_viewed')
        assert project.ProjectJobsViewedEvent.get_event_action() == 'jobs_viewed'
        assert project.ProjectBuildsViewedEvent.get_event_action() == 'builds_viewed'
        assert project.ProjectTensorboardsViewedEvent.get_event_action() == 'tensorboards_viewed'
        assert project.ProjectNotebooksViewedEvent.get_event_action() == 'notebooks_viewed'

    def test_events_actions_repos(self):
        assert repo.RepoCreatedEvent.get_event_action() == 'created'
        assert repo.RepoNewCommitEvent.get_event_action() == 'new_commit'

    def test_events_actions_superuser(self):
        assert superuser.SuperUserRoleGrantedEvent.get_event_action() == 'granted'
        assert superuser.SuperUserRoleRevokedEvent.get_event_action() == 'revoked'

    def test_events_actions_tensorboards(self):
        assert tensorboard.TensorboardStartedEvent.get_event_action() is None
        assert tensorboard.TensorboardStartedTriggeredEvent.get_event_action() == 'started'
        assert tensorboard.TensorboardSoppedEvent.get_event_action() is None
        assert tensorboard.TensorboardSoppedTriggeredEvent.get_event_action() == 'stopped'
        assert tensorboard.TensorboardCleanedTriggeredEvent.get_event_action() is None
        assert tensorboard.TensorboardViewedEvent.get_event_action() == 'viewed'
        assert tensorboard.TensorboardBookmarkedEvent.get_event_action() == 'bookmarked'
        assert tensorboard.TensorboardUnBookmarkedEvent.get_event_action() == 'unbookmarked'
        assert tensorboard.TensorboardNewStatusEvent.get_event_action() is None
        assert tensorboard.TensorboardFailedEvent.get_event_action() is None
        assert tensorboard.TensorboardSucceededEvent.get_event_action() is None
        assert tensorboard.TensorboardStatusesViewedEvent.get_event_action() == 'statuses_viewed'
        assert tensorboard.TensorboardUpdatedEvent.get_event_action() == 'updated'
        assert tensorboard.TensorboardDeletedEvent.get_event_action() is None
        assert tensorboard.TensorboardDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert tensorboard.TensorboardArchivedEvent.get_event_action() == 'archived'
        assert tensorboard.TensorboardRestoredEvent.get_event_action() == 'restored'

    def test_events_actions_users(self):
        assert user.UserRegisteredEvent.get_event_action() == 'registered'
        assert user.UserUpdatedEvent.get_event_action() == 'updated'
        assert user.UserActivatedEvent.get_event_action() == 'activated'
        assert user.UserDeletedEvent.get_event_action() == 'deleted'
        assert user.UserLDAPEvent.get_event_action() is None
        assert user.UserGITHUBEvent.get_event_action() == 'auth'
        assert user.UserGITLABEvent.get_event_action() == 'auth'
        assert user.UserBITBUCKETEvent.get_event_action() == 'auth'
        assert user.UserAZUREEvent.get_event_action() == 'auth'

    def test_events_actions_pipelines(self):
        assert pipeline.PipelineCreatedEvent.get_event_action() == 'created'
        assert pipeline.PipelineUpdatedEvent.get_event_action() == 'updated'
        assert pipeline.PipelineDeletedEvent.get_event_action() is None
        assert pipeline.PipelineViewedEvent.get_event_action() == 'viewed'
        assert pipeline.PipelineArchivedEvent.get_event_action() == 'archived'
        assert pipeline.PipelineRestoredEvent.get_event_action() == 'restored'
        assert pipeline.PipelineBookmarkedEvent.get_event_action() == 'bookmarked'
        assert pipeline.PipelineUnbookmarkedEvent.get_event_action() == 'unbookmarked'
        assert pipeline.PipelineDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert pipeline.PipelineCleanedTriggeredEvent.get_event_action() is None

    def test_events_actions_operations(self):
        assert operation.OperationCreatedEvent.get_event_action() is None
        assert operation.OperationUpdatedEvent.get_event_action() == 'updated'
        assert operation.OperationDeletedEvent.get_event_action() is None
        assert operation.OperationViewedEvent.get_event_action() == 'viewed'
        assert operation.OperationArchivedEvent.get_event_action() == 'archived'
        assert operation.OperationRestoredEvent.get_event_action() == 'restored'
        assert operation.OperationDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert operation.OperationCleanedTriggeredEvent.get_event_action()  is None

    def test_events_actions_pipeline_runs(self):
        assert pipeline_run.PipelineRunCreatedEvent.get_event_action() == 'created'
        assert pipeline_run.PipelineRunUpdatedEvent.get_event_action() == 'updated'
        assert pipeline_run.PipelineRunDeletedEvent.get_event_action() is None
        assert pipeline_run.PipelineRunViewedEvent.get_event_action() == 'viewed'
        assert pipeline_run.PipelineRunArchivedEvent.get_event_action() == 'archived'
        assert pipeline_run.PipelineRunRestoredEvent.get_event_action() == 'restored'
        assert pipeline_run.PipelineRunStoppedEvent.get_event_action() is None
        assert pipeline_run.PipelineRunSkippedEvent.get_event_action() is None
        assert pipeline_run.PipelineRunResumedEvent.get_event_action() is None
        assert pipeline_run.PipelineRunRestartedEvent.get_event_action() is None
        assert pipeline_run.PipelineRunNewStatusEvent.get_event_action() is None
        assert pipeline_run.PipelineRunSucceededEvent.get_event_action() is None
        assert pipeline_run.PipelineRunFailedEvent.get_event_action() is None
        assert pipeline_run.PipelineRunDoneEvent.get_event_action() is None
        assert pipeline_run.PipelineRunDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert pipeline_run.PipelineRunCleanedTriggeredEvent.get_event_action() is None
        assert pipeline_run.PipelineRunStoppedTriggeredEvent.get_event_action() == 'stopped'
        assert pipeline_run.PipelineRunResumedTriggeredEvent.get_event_action() == 'resumed'
        assert pipeline_run.PipelineRunRestartedTriggeredEvent.get_event_action() == 'restarted'
        assert pipeline_run.PipelineRunSkippedTriggeredEvent.get_event_action() == 'skipped'

    def test_events_actions_operation_runs(self):
        assert operation_run.OperationRunCreatedEvent.get_event_action() == 'created'
        assert operation_run.OperationRunUpdatedEvent.get_event_action() == 'updated'
        assert operation_run.OperationRunDeletedEvent.get_event_action() is None
        assert operation_run.OperationRunViewedEvent.get_event_action() == 'viewed'
        assert operation_run.OperationRunArchivedEvent.get_event_action() == 'archived'
        assert operation_run.OperationRunRestoredEvent.get_event_action() == 'restored'
        assert operation_run.OperationRunStoppedEvent.get_event_action() is None
        assert operation_run.OperationRunSkippedEvent.get_event_action() is None
        assert operation_run.OperationRunResumedEvent.get_event_action() is None
        assert operation_run.OperationRunRestartedEvent.get_event_action() is None
        assert operation_run.OperationRunNewStatusEvent.get_event_action() is None
        assert operation_run.OperationRunSucceededEvent.get_event_action() is None
        assert operation_run.OperationRunFailedEvent.get_event_action() is None
        assert operation_run.OperationRunDoneEvent.get_event_action() is None
        assert operation_run.OperationRunDeletedTriggeredEvent.get_event_action() == 'deleted'
        assert operation_run.OperationRunCleanedTriggeredEvent.get_event_action() is None
        assert operation_run.OperationRunStoppedTriggeredEvent.get_event_action() == 'stopped'
        assert operation_run.OperationRunResumedTriggeredEvent.get_event_action() == 'resumed'
        assert operation_run.OperationRunRestartedTriggeredEvent.get_event_action() == 'restarted'
        assert operation_run.OperationRunSkippedTriggeredEvent.get_event_action() == 'skipped'

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

        event_serialized_dump = event.serialize(dumps=True)
        assert event_serialized == loads(event_serialized_dump)

    def test_serialize_with_instance(self):
        instance = ExperimentFactory()
        event = ExperimentSucceededEvent.from_instance(instance=instance,
                                                       actor_id=1,
                                                       actor_name='user')
        event_serialized = event.serialize(dumps=False, include_instance_info=True)
        instance_contenttype = ContentType.objects.get_for_model(instance).id
        assert event_serialized['instance_id'] == instance.id
        assert event_serialized['instance_contenttype'] == instance_contenttype

    def test_from_event_data(self):
        instance = ExperimentFactory()
        event = ExperimentSucceededEvent.from_instance(instance=instance,
                                                       actor_id=1,
                                                       actor_name='user')
        assert event.ref_id is None
        event_serialized = event.serialize(dumps=False, include_instance_info=True)
        assert event_serialized.get('ref_id') is None
        new_event = ExperimentSucceededEvent.from_event_data(event_data=event_serialized)
        assert new_event.serialize(include_instance_info=True) == event_serialized

        # Add ref id
        event.ref_id = uuid1()
        event_serialized = event.serialize(dumps=False, include_instance_info=True)
        assert event_serialized['ref_id'] == event.ref_id.hex
        new_event = ExperimentSucceededEvent.from_event_data(event_data=event_serialized)
        assert new_event.ref_id == event.ref_id
        assert new_event.serialize(include_instance_info=True) == event_serialized

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
        class DummyEvent1(Event):
            event_type = 'dummy.event'
            actor = True
            attributes = (
                Attribute('attr1'),
            )

        class DummyEvent2(Event):
            event_type = 'dummy.event'
            actor = True
            actor_id = 'some_actor_id'
            actor_name = 'some_actor_name'
            attributes = (
                Attribute('attr1'),
            )

        class DummyObject1(object):
            attr1 = 'test'

        class DummyObject2(object):
            attr1 = 'test'
            some_actor_id = 1
            some_actor_name = 'foo'

        # Not providing actor_id raises
        obj = DummyObject1()
        with self.assertRaises(ValueError):
            DummyEvent1.from_instance(obj)

        # Providing actor_id and not actor_name raises
        with self.assertRaises(ValueError):
            DummyEvent1.from_instance(obj, actor_id=1)

        # Providing system actor id without actor_name does not raise
        event = DummyEvent1.from_instance(obj, actor_id=user_system.USER_SYSTEM_ID)
        assert event.data['actor_id'] == user_system.USER_SYSTEM_ID
        assert event.data['actor_name'] == user_system.USER_SYSTEM_NAME

        # Providing actor_id and actor_name does not raise
        event = DummyEvent1.from_instance(obj, actor_id=1, actor_name='foo')
        assert event.data['actor_id'] == 1
        assert event.data['actor_name'] == 'foo'

        # Using an instance that has the actor properties
        obj2 = DummyObject2()
        event = DummyEvent2.from_instance(obj2)
        assert event.data['some_actor_id'] == 1
        assert event.data['some_actor_name'] == 'foo'

        # Using an instance that has the actor properties and overriding the actor
        event = DummyEvent2.from_instance(obj2,
                                          some_actor_id=user_system.USER_SYSTEM_ID,
                                          some_actor_name=user_system.USER_SYSTEM_NAME)
        assert event.data['some_actor_id'] == user_system.USER_SYSTEM_ID
        assert event.data['some_actor_name'] == user_system.USER_SYSTEM_NAME
