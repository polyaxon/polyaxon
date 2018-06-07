import pytest
from mock import patch

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.build_jobs_mark
class TestBuildJobStatuses(BaseTest):
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.build_job = BuildJobFactory(project=self.project)
        self.notebook = NotebookJobFactory(project=self.project, build_job=self.build_job)
        self.tensorboard = TensorboardJobFactory(project=self.project, build_job=self.build_job)
        self.job = JobFactory(project=self.project, build_job=self.build_job)
        self.experiment = ExperimentFactory(project=self.project, build_job=self.build_job)

    def test_build_job_failed_sets_dependency_to_failed(self):
        assert self.build_job.last_status != JobLifeCycle.FAILED
        assert self.notebook.last_status != JobLifeCycle.FAILED
        assert self.tensorboard.last_status != JobLifeCycle.FAILED
        assert self.job.last_status != JobLifeCycle.FAILED
        assert self.experiment.last_status != ExperimentLifeCycle.FAILED

        self.build_job.set_status(JobLifeCycle.FAILED)

        assert self.build_job.last_status == JobLifeCycle.FAILED
        self.notebook.refresh_from_db()
        assert self.notebook.last_status == JobLifeCycle.FAILED
        self.tensorboard.refresh_from_db()
        assert self.tensorboard.last_status == JobLifeCycle.FAILED
        self.job.refresh_from_db()
        assert self.job.last_status == JobLifeCycle.FAILED
        self.experiment.refresh_from_db()
        assert self.experiment.last_status == ExperimentLifeCycle.FAILED

    def test_build_job_stopped_sets_dependency_to_stopped(self):
        assert self.build_job.last_status != JobLifeCycle.STOPPED
        assert self.notebook.last_status != JobLifeCycle.STOPPED
        assert self.tensorboard.last_status != JobLifeCycle.STOPPED
        assert self.job.last_status != JobLifeCycle.STOPPED
        assert self.experiment.last_status != ExperimentLifeCycle.STOPPED

        self.build_job.set_status(JobLifeCycle.STOPPED)

        assert self.build_job.last_status == JobLifeCycle.STOPPED
        self.notebook.refresh_from_db()
        assert self.notebook.last_status == JobLifeCycle.STOPPED
        self.tensorboard.refresh_from_db()
        assert self.tensorboard.last_status == JobLifeCycle.STOPPED
        self.job.refresh_from_db()
        assert self.job.last_status == JobLifeCycle.STOPPED
        self.experiment.refresh_from_db()
        assert self.experiment.last_status == ExperimentLifeCycle.STOPPED

    def test_build_job_succeeded_starts_dependency(self):
        assert self.build_job.last_status != JobLifeCycle.SUCCEEDED
        assert self.notebook.last_status != JobLifeCycle.SUCCEEDED
        assert self.tensorboard.last_status != JobLifeCycle.SUCCEEDED
        assert self.job.last_status != JobLifeCycle.SUCCEEDED
        assert self.experiment.last_status != ExperimentLifeCycle.SUCCEEDED

        with patch('scheduler.notebook_scheduler.start_notebook') as mock_notebook:
            with patch('scheduler.tensorboard_scheduler.start_tensorboard') as mock_tensorboard:
                with patch('scheduler.experiment_scheduler.start_experiment') as mock_experiment:
                    with patch('scheduler.job_scheduler.start_job') as mock_job:
                        self.build_job.set_status(JobLifeCycle.SUCCEEDED)

        assert self.build_job.last_status == JobLifeCycle.SUCCEEDED
        assert mock_notebook.call_count == 1
        assert mock_tensorboard.call_count == 1
        assert mock_experiment.call_count == 1
        assert mock_job.call_count == 1
