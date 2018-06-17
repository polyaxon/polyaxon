from unittest.mock import patch

import mock
import pytest

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import MULTIPART_CONTENT

from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.jobs import Job, JobStatus
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from factories.fixtures import job_spec_content, job_spec_resources_content
from polyaxon_schemas.polyaxonfile.specification import JobSpecification
from scheduler.tasks.jobs import jobs_build
from tests.utils import BaseTest, BaseViewTest


@pytest.mark.jobs_mark
class TestJobModel(BaseTest):

    def test_create_job(self):
        job = JobFactory()
        assert isinstance(job.specification, JobSpecification)

    def test_job_creation_triggers_status_creation_mock(self):
        with patch.object(Job, 'set_status') as mock_fct:
            JobFactory()
        assert mock_fct.call_count == 1

    def test_job_creation_triggers_status_creation(self):
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            job = JobFactory()
        assert JobStatus.objects.filter(job=job).count() == 1
        assert job.last_status == JobLifeCycle.CREATED

    def test_job_creation_triggers_scheduling_mocks(self):
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            with patch.object(Job, 'set_status') as mock_fct2:
                JobFactory()

        assert mock_fct.call_count == 1
        assert mock_fct2.call_count == 1

    def test_job_creation_triggers_build(self):
        # Create a repo for the project
        repo = RepoFactory()

        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_build:
            job = JobFactory(project=repo.project)

        assert mock_build.call_count == 1
        assert job.project.repo is not None

        assert JobStatus.objects.filter(job=job).count() == 1
        assert list(JobStatus.objects.filter(job=job).values_list(
            'status', flat=True)) == [JobLifeCycle.CREATED]

        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_start.return_value = True
                mock_check.return_value = False
                jobs_build(job_id=job.id)

        assert mock_start.call_count == 1
        assert mock_check.call_count == 1
        assert JobStatus.objects.filter(job=job).count() == 2
        assert list(JobStatus.objects.filter(job=job).values_list(
            'status', flat=True)) == [JobLifeCycle.CREATED,
                                      JobLifeCycle.BUILDING]
        job.refresh_from_db()
        assert job.last_status == JobLifeCycle.BUILDING

    def test_job_creation_with_already_built_triggers_scheduling(self):
        # Create a repo for the project
        repo = RepoFactory()

        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_build:
            job = JobFactory(project=repo.project)

        assert mock_build.call_count == 1
        assert job.project.repo is not None

        assert JobStatus.objects.filter(job=job).count() == 1
        assert list(JobStatus.objects.filter(job=job).values_list(
            'status', flat=True)) == [JobLifeCycle.CREATED]

        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_start.return_value = False
                mock_check.return_value = True
                jobs_build(job_id=job.id)

        assert mock_start.call_count == 0
        assert mock_check.call_count == 1
        assert JobStatus.objects.filter(job=job).count() == 2
        assert list(JobStatus.objects.filter(job=job).values_list(
            'status', flat=True)) == [JobLifeCycle.CREATED,
                                      JobLifeCycle.SCHEDULED]
        job.refresh_from_db()
        assert job.last_status == JobLifeCycle.SCHEDULED

    @mock.patch('scheduler.job_scheduler.JobSpawner')
    def test_create_job_with_valid_spec(self, spawner_mock):
        config = JobSpecification.read(job_spec_content)

        mock_instance = spawner_mock.return_value
        mock_instance.start_job.return_value = {'pod': 'pod_content'}
        mock_instance.spec = config

        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_start.return_value = False
                mock_check.return_value = True
                job = JobFactory(config=config.parsed_data)

        assert JobStatus.objects.filter(job=job).count() == 2
        assert list(JobStatus.objects.filter(job=job).values_list(
            'status', flat=True)) == [JobLifeCycle.CREATED,
                                      JobLifeCycle.SCHEDULED]
        job.refresh_from_db()
        assert job.last_status == JobLifeCycle.SCHEDULED

    @mock.patch('scheduler.job_scheduler.JobSpawner')
    def test_create_job_with_resources_spec(self, spawner_mock):
        config = JobSpecification.read(job_spec_resources_content)
        mock_instance = spawner_mock.return_value
        mock_instance.start_job.return_value = {'pod': 'pod_content'}
        mock_instance.spec = config

        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_start.return_value = False
                mock_check.return_value = True
                job = JobFactory(config=config.parsed_data)

        assert JobStatus.objects.filter(job=job).count() == 2
        assert list(JobStatus.objects.filter(job=job).values_list(
            'status', flat=True)) == [JobLifeCycle.CREATED,
                                      JobLifeCycle.SCHEDULED]

        job.refresh_from_db()
        assert job.last_status == JobLifeCycle.SCHEDULED

    @patch('libs.paths.jobs.delete_path')
    def test_delete_job_does_not_trigger_job_stop_if_not_running(self, delete_path):
        job = JobFactory()
        assert delete_path.call_count == 2  # outputs + logs
        with patch('scheduler.job_scheduler.stop_job') as mock_fct:
            job.delete()
        assert delete_path.call_count == 2 + 2  # outputs + logs
        assert mock_fct.call_count == 0

    @patch('libs.paths.jobs.delete_path')
    def test_delete_job_triggers_job_stop_mock(self, delete_path):
        job = JobFactory()
        job.set_status(JobLifeCycle.SCHEDULED)
        assert delete_path.call_count == 2  # outputs + logs
        with patch('scheduler.job_scheduler.stop_job') as mock_fct:
            job.delete()
        assert delete_path.call_count == 2 + 2  # outputs + logs
        assert mock_fct.call_count == 1


@pytest.mark.jobs_mark
class TestJobCommit(BaseViewTest):
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

    def create_job(self, config):
        config = JobSpecification.read(config)
        return JobFactory(config=config.parsed_data, project=self.project)

    def test_job_is_saved_with_commit(self):
        uploaded_file = self.get_upload_file()

        self.auth_client.put(self.url,
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        last_commit = self.project.repo.last_commit
        assert last_commit is not None

        # Check job is created with commit
        job = self.create_job(job_spec_content)

        assert job.code_reference.commit == last_commit[0]
        assert job.code_reference.repo == self.project.repo

        # Make a new upload with repo_new.tar.gz containing 2 files
        new_uploaded_file = self.get_upload_file('updated_repo')
        self.auth_client.put(self.url,
                             data={'repo': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        new_commit = self.project.repo.last_commit
        assert new_commit is not None
        assert new_commit[0] != last_commit[0]

        # Check new experiment is created with new commit
        new_job = self.create_job(job_spec_content)
        assert new_job.code_reference.commit == new_commit[0]
        assert new_job.code_reference.repo == self.project.repo
