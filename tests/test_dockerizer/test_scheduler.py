from unittest.mock import patch

import pytest

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob
from factories.factorycode_reference import CodeReferenceFactory
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_projects import ProjectFactory
from polyaxon_schemas.polyaxonfile.specification import BuildSpecification
from scheduler import dockerizer_scheduler
from tests.utils import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerizerScheduler(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.code_reference = CodeReferenceFactory()

    def test_scheduler_create_build_job(self):
        """Test the case when the job needs to be built and started."""
        assert BuildJob.objects.count() == 0
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_start.return_value = True
                mock_check.return_value = False
                build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
                    user=self.project.user,
                    project=self.project,
                    config={'image': 'bar:foo'},
                    code_reference=self.code_reference
                )
        assert mock_start.call_count == 1
        assert mock_check.call_count == 1
        assert image_exists is False
        assert build_status is True
        assert BuildJob.objects.count() == 1

    def test_scheduler_create_build_job_of_already_running_job(self):
        """Check the case when the job is already running and
        we just set the requesting service to running."""
        config = {'image': 'busybox:tag'}
        build_job = BuildJobFactory(project=self.project,
                                    user=self.project.user,
                                    code_reference=self.code_reference,
                                    config=BuildSpecification.create_specification(config))
        build_job.set_status(JobLifeCycle.RUNNING)

        assert BuildJob.objects.count() == 1
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_check.return_value = False
                build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
                    user=self.project.user,
                    project=self.project,
                    config=config,
                    code_reference=self.code_reference
                )
        assert mock_start.call_count == 0
        assert mock_check.call_count == 1
        assert image_exists is False
        assert build_status is True
        assert BuildJob.objects.count() == 1

    def test_scheduler_create_build_job_of_already_done_job(self):
        """Check the case when the job is already done and
        we need to create a new job."""
        config = {'image': 'busybox:tag'}
        build_job = BuildJobFactory(project=self.project,
                                    user=self.project.user,
                                    code_reference=self.code_reference,
                                    config=BuildSpecification.create_specification(config))
        build_job.set_status(JobLifeCycle.STOPPED)

        assert BuildJob.objects.count() == 1
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_start.return_value = True
                mock_check.return_value = False
                build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
                    user=self.project.user,
                    project=self.project,
                    config=config,
                    code_reference=self.code_reference
                )
        assert mock_start.call_count == 1
        assert mock_check.call_count == 1
        assert image_exists is False
        assert build_status is True
        assert BuildJob.objects.count() == 2

    def test_scheduler_create_build_job_image_already_exists(self):
        """Check the case when the image is already built."""
        config = {'image': 'busybox:tag'}
        BuildJobFactory(project=self.project,
                        user=self.project.user,
                        code_reference=self.code_reference,
                        config=BuildSpecification.create_specification(config))

        assert BuildJob.objects.count() == 1
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            with patch('scheduler.dockerizer_scheduler.check_image') as mock_check:
                mock_check.return_value = True
                build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
                    user=self.project.user,
                    project=self.project,
                    config=config,
                    code_reference=self.code_reference
                )
        assert mock_start.call_count == 0
        assert mock_check.call_count == 1
        assert image_exists is True
        assert build_status is False
        assert BuildJob.objects.count() == 1
