import os

from unittest.mock import patch

import mock

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, tag
from django.test.client import MULTIPART_CONTENT
from django.utils import timezone

from experiments.models import Experiment, ExperimentJob, ExperimentStatus
from experiments.paths import create_experiment_outputs_path, get_experiment_outputs_path
from experiments.restart import handle_restarted_experiment
from experiments.statuses import ExperimentLifeCycle
from experiments.tasks import set_metrics, sync_experiments_and_jobs_statuses
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentJobFactory,
    ExperimentJobStatusFactory,
    ExperimentStatusFactory
)
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from factories.fixtures import (
    exec_experiment_resources_content,
    exec_experiment_spec_content,
    experiment_spec_content
)
from jobs.models import JobResources
from jobs.statuses import JobLifeCycle
from polyaxon.urls import API_V1
from polyaxon_schemas.polyaxonfile.specification import ExperimentSpecification
from polyaxon_schemas.utils import TaskType
from tests.fixtures import start_experiment_value
from tests.utils import RUNNER_TEST, BaseTest, BaseViewTest


class TestExperimentModel(BaseTest):
    @override_settings(DEPLOY_RUNNER=False)
    def test_experiment_creation_triggers_status_creation_mocks(self):
        with patch.object(Experiment, 'set_status') as mock_fct2:
            ExperimentFactory()
        assert mock_fct2.call_count == 1

    @tag(RUNNER_TEST)
    def test_non_independent_experiment_creation_doesnt_trigger_start(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as _:
            experiment_group = ExperimentGroupFactory()

        with patch('experiments.tasks.start_experiment.delay') as mock_fct:
            with patch.object(Experiment, 'set_status') as mock_fct2:
                ExperimentFactory(experiment_group=experiment_group)

        assert mock_fct.call_count == 0
        assert mock_fct2.call_count == 1

    @override_settings(DEPLOY_RUNNER=False)
    def test_experiment_creation_triggers_status_creation(self):
        experiment = ExperimentFactory()

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 1
        assert experiment.last_status == ExperimentLifeCycle.CREATED

    @tag(RUNNER_TEST)
    def test_independent_experiment_creation_triggers_experiment_scheduling_mocks(self):
        with patch('experiment_groups.tasks.start_group_experiments.apply_async') as _:
            with patch('experiments.tasks.build_experiment.apply_async') as mock_fct:
                with patch.object(Experiment, 'set_status') as mock_fct2:
                    ExperimentFactory()

        assert mock_fct.call_count == 1
        assert mock_fct2.call_count == 1

    @tag(RUNNER_TEST)
    def test_independent_experiment_creation_triggers_experiment_scheduling(self):
        content = ExperimentSpecification.read(experiment_spec_content)
        experiment = ExperimentFactory(config=content.parsed_data)
        assert experiment.is_independent is True

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 2
        assert list(ExperimentStatus.objects.filter(experiment=experiment).values_list(
            'status', flat=True)) == [ExperimentLifeCycle.CREATED, ExperimentLifeCycle.SCHEDULED]
        experiment.refresh_from_db()
        assert experiment.last_status == ExperimentLifeCycle.SCHEDULED

        # Assert also that experiment is monitored
        assert experiment.last_status == ExperimentLifeCycle.SCHEDULED

    @tag(RUNNER_TEST)
    def test_independent_experiment_creation_with_run_triggers_experiment_building_scheduling(self):
        content = ExperimentSpecification.read(exec_experiment_spec_content)
        # Create a repo for the project
        repo = RepoFactory()

        with patch('runner.dockerizer.builders.experiments.build_experiment') as mock_docker_build:
            experiment = ExperimentFactory(config=content.parsed_data, project=repo.project)

        assert mock_docker_build.call_count == 1
        assert experiment.project.repo is not None
        assert experiment.is_independent is True

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 3
        assert list(ExperimentStatus.objects.filter(experiment=experiment).values_list(
            'status', flat=True)) == [ExperimentLifeCycle.CREATED,
                                      ExperimentLifeCycle.BUILDING,
                                      ExperimentLifeCycle.SCHEDULED]
        experiment.refresh_from_db()
        assert experiment.last_status == ExperimentLifeCycle.SCHEDULED

    @tag(RUNNER_TEST)
    @mock.patch('runner.schedulers.experiment_scheduler.ExperimentSpawner')
    def test_create_experiment_with_valid_spec(self, spawner_mock):
        content = ExperimentSpecification.read(experiment_spec_content)

        mock_instance = spawner_mock.return_value
        mock_instance.start_experiment.return_value = start_experiment_value
        mock_instance.spec = content

        experiment = ExperimentFactory(config=content.parsed_data)
        assert experiment.is_independent is True

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 3
        assert list(ExperimentStatus.objects.filter(experiment=experiment).values_list(
            'status', flat=True)) == [ExperimentLifeCycle.CREATED,
                                      ExperimentLifeCycle.SCHEDULED,
                                      ExperimentLifeCycle.STARTING]
        experiment.refresh_from_db()
        assert experiment.last_status == ExperimentLifeCycle.STARTING

        # Assert 1 job was created
        assert ExperimentJob.objects.filter(experiment=experiment).count() == 1
        assert JobResources.objects.count() == 0
        jobs_statuses = ExperimentJob.objects.values_list('statuses__status', flat=True)
        assert set(jobs_statuses) == {JobLifeCycle.CREATED, }
        jobs = ExperimentJob.objects.filter(experiment=experiment)
        assert experiment.calculated_status == ExperimentLifeCycle.STARTING

        for job in jobs:
            # Assert the jobs status is created
            assert job.last_status == JobLifeCycle.CREATED

    @tag(RUNNER_TEST)
    @mock.patch('runner.schedulers.experiment_scheduler.TensorflowSpawner')
    def test_create_experiment_with_resources_spec(self, spawner_mock):
        content = ExperimentSpecification.read(exec_experiment_resources_content)

        mock_instance = spawner_mock.return_value
        mock_instance.start_experiment.return_value = start_experiment_value
        mock_instance.spec = content

        experiment = ExperimentFactory(config=content.parsed_data)
        assert experiment.is_independent is True

        assert ExperimentStatus.objects.filter(experiment=experiment).count() == 3
        assert list(ExperimentStatus.objects.filter(experiment=experiment).values_list(
            'status', flat=True)) == [ExperimentLifeCycle.CREATED,
                                      ExperimentLifeCycle.SCHEDULED,
                                      ExperimentLifeCycle.STARTING]
        experiment.refresh_from_db()
        assert experiment.last_status == ExperimentLifeCycle.STARTING

        # Assert 3 jobs were created with resources
        assert ExperimentJob.objects.filter(experiment=experiment).count() == 3
        assert JobResources.objects.count() == 3
        jobs_statuses = ExperimentJob.objects.values_list('statuses__status', flat=True)
        assert set(jobs_statuses) == {JobLifeCycle.CREATED, }
        jobs = ExperimentJob.objects.filter(experiment=experiment)
        assert experiment.calculated_status == ExperimentLifeCycle.STARTING

        for job in jobs:
            # Assert the jobs status is created
            assert job.last_status == JobLifeCycle.CREATED

    @override_settings(DEPLOY_RUNNER=False)
    @patch('experiments.paths.delete_path')
    def test_delete_experiment_triggers_experiment_stop_mocks(self, delete_path):
        experiment = ExperimentFactory()
        experiment.delete()
        assert delete_path.call_count == 2

    @tag(RUNNER_TEST)
    def test_delete_experiment_triggers_experiment_stop_mocks(self):
        experiment = ExperimentFactory()
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as mock_fct:
            experiment.delete()

        assert mock_fct.call_count == 1

    def test_set_metrics(self):
        content = ExperimentSpecification.read(experiment_spec_content)
        experiment = ExperimentFactory(config=content.parsed_data)
        assert experiment.metrics.count() == 0

        create_at = timezone.now()
        set_metrics(experiment_uuid=experiment.uuid.hex,
                    created_at=create_at,
                    metrics={'accuracy': 0.9, 'precision': 0.9})

        assert experiment.metrics.count() == 1

    @tag(RUNNER_TEST)
    def test_master_success_influences_other_experiment_workers_status(self):
        with patch('experiments.tasks.start_experiment.delay') as _:
            with patch.object(Experiment, 'set_status') as _:
                experiment = ExperimentFactory()

        assert ExperimentLifeCycle.is_done(experiment.last_status) is False
        # Add jobs
        master = ExperimentJobFactory(experiment=experiment, role=TaskType.MASTER)
        assert JobLifeCycle.is_done(master.last_status) is False
        workers = [ExperimentJobFactory(experiment=experiment, role=TaskType.WORKER)
                   for _ in range(2)]
        for worker in workers:
            worker.refresh_from_db()
            assert JobLifeCycle.is_done(worker.last_status) is False

        # Set master to succeeded
        ExperimentJobStatusFactory(job=master, status=JobLifeCycle.SUCCEEDED)

        # All worker should have a success status
        for worker in workers:
            worker.refresh_from_db()
            assert worker.last_status == JobLifeCycle.SUCCEEDED

        # Experiment last status should be success
        experiment.refresh_from_db()
        assert experiment.last_status == ExperimentLifeCycle.SUCCEEDED

    @tag(RUNNER_TEST)
    def test_sync_experiments_and_jobs_statuses(self):
        with patch('experiments.tasks.start_experiment.delay') as _:
            with patch.object(Experiment, 'set_status') as _:
                experiments = [ExperimentFactory() for _ in range(3)]

        done_xp, no_jobs_xp, xp_with_jobs = experiments

        # Set done status
        with patch('runner.schedulers.experiment_scheduler.stop_experiment') as _:
            ExperimentStatusFactory(experiment=done_xp, status=JobLifeCycle.FAILED)

        # Create jobs for xp_with_jobs and update status, and do not update the xp status
        with patch.object(Experiment, 'set_status') as _:
            job = ExperimentJobFactory(experiment=xp_with_jobs)
            ExperimentJobStatusFactory(job=job, status=JobLifeCycle.RUNNING)

        xp_with_jobs.refresh_from_db()
        assert xp_with_jobs.last_status is None

        # Mock sync experiments and jobs statuses
        with patch('experiments.tasks.check_experiment_status.delay') as check_status_mock:
            sync_experiments_and_jobs_statuses()

        assert check_status_mock.call_count == 1

        # Call sync experiments and jobs statuses
        sync_experiments_and_jobs_statuses()
        done_xp.refresh_from_db()
        no_jobs_xp.refresh_from_db()
        xp_with_jobs.refresh_from_db()
        assert done_xp.last_status == ExperimentLifeCycle.FAILED
        assert no_jobs_xp.last_status is None
        assert xp_with_jobs.last_status == ExperimentLifeCycle.RUNNING

    @tag(RUNNER_TEST)
    def test_restarting_an_experiment(self):
        with patch('experiments.tasks.build_experiment.apply_async') as _:
            experiment1 = ExperimentFactory()

        # We create some outputs files for the experiment
        path = create_experiment_outputs_path(experiment1.unique_name)
        open(os.path.join(path, 'file'), 'w+')

        # Create a new experiment that is a clone of the previous
        with patch('experiments.tasks.build_experiment.apply_async') as _:
            experiment2 = ExperimentFactory(original_experiment=experiment1)

        # Check that outputs path for experiment2 does not exist yet
        experiment2_outputs_path = get_experiment_outputs_path(experiment2.unique_name)
        assert os.path.exists(experiment2_outputs_path) is False

        # Handle restart should create the outputs and copy the content of experiment 1
        handle_restarted_experiment(experiment2)

        assert os.path.exists(experiment2_outputs_path) is True
        assert os.path.exists(os.path.join(experiment2_outputs_path, 'file')) is True


class TestExperimentCommit(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/repo/upload'.format(API_V1,
                                                  self.project.user.username,
                                                  self.project.name)

    @staticmethod
    def get_upload_file(filename='repo'):
        file = File(open('./tests/fixtures_static/{}.tar.gz'.format(filename), 'rb'))
        return SimpleUploadedFile(filename, file.read(),
                                  content_type='multipart/form-data')

    @override_settings(DEPLOY_RUNNER=False)
    def create_experiment(self, content):
        config = ExperimentSpecification.read(content)
        return ExperimentFactory(config=config.parsed_data, project=self.project)

    def test_experiment_is_saved_with_commit(self):
        uploaded_file = self.get_upload_file()

        self.auth_client.put(self.url,
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        last_commit = self.project.repo.last_commit
        assert last_commit is not None

        # Check experiment is created with commit
        experiment = self.create_experiment(exec_experiment_spec_content)

        assert experiment.commit == last_commit[0]

        # Make a new upload with repo_new.tar.gz containing 2 files
        new_uploaded_file = self.get_upload_file('updated_repo')
        self.auth_client.put(self.url,
                             data={'repo': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        new_commit = self.project.repo.last_commit
        assert new_commit is not None
        assert new_commit[0] != last_commit[0]

        # Check new experiment is created with new commit
        new_experiment = self.create_experiment(exec_experiment_spec_content)
        assert new_experiment.commit == new_commit[0]

        # Cloning an experiment does not assign commit
        clone_experiment = Experiment.objects.create(
            project=experiment.project,
            user=self.project.user,
            description=experiment.description,
            experiment_group=experiment.experiment_group,
            config=experiment.config,
            original_experiment=experiment,
            commit=experiment.commit
        )

        assert clone_experiment.commit == experiment.commit

        # Model experiments should not get a commit
        model_experiment = self.create_experiment(experiment_spec_content)
        assert model_experiment.commit is None
