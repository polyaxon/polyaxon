from unittest.mock import patch

import pytest

from db.models.build_jobs import BuildJob
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_code_reference import CodeReferenceFactory
from factories.factory_projects import ProjectFactory
from lifecycles.jobs import JobLifeCycle
from scheduler import dockerizer_scheduler
from schemas import BuildSpecification
from tests.base.case import BaseTest


@pytest.mark.dockerizer_mark
class TestDockerizerScheduler(BaseTest):
    DISABLE_EXECUTOR = False
    DISABLE_RUNNER = False

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.code_reference = CodeReferenceFactory()

    def test_scheduler_create_build_job(self):
        """Test the case when the job needs to be built and started."""
        assert BuildJob.objects.count() == 0
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            mock_start.return_value = True
            _, image_exists, build_status = dockerizer_scheduler.create_build_job(
                user=self.project.user,
                project=self.project,
                config={'image': 'bar:foo'},
                code_reference=self.code_reference
            )
        assert mock_start.call_count == 1
        assert image_exists is False
        assert build_status is True
        assert BuildJob.objects.count() == 1

    def test_scheduler_create_build_job_of_already_running_job(self):
        """Check the case when the job is already running and
        we just set the requesting service to running."""
        config = {'image': 'busybox:tag'}
        build_job = BuildJobFactory(
            project=self.project,
            user=self.project.user,
            code_reference=self.code_reference,
            content=BuildSpecification.create_specification(config, to_dict=False).raw_data)
        build_job.set_status(JobLifeCycle.RUNNING)

        assert BuildJob.objects.count() == 1
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
                user=self.project.user,
                project=self.project,
                config=config,
                code_reference=self.code_reference
            )
        assert mock_start.call_count == 0
        assert image_exists is False
        assert build_status is True
        assert BuildJob.objects.count() == 1

    def test_scheduler_create_build_job_of_already_done_job(self):
        """Check the case when the job is already done and
        we need to create a new job."""
        config = {'image': 'busybox:tag'}
        build_job = BuildJobFactory(
            project=self.project,
            user=self.project.user,
            code_reference=self.code_reference,
            content=BuildSpecification.create_specification(config, to_dict=False).raw_data)
        build_job.set_status(JobLifeCycle.STOPPED)

        assert BuildJob.objects.count() == 1
        with patch('scheduler.dockerizer_scheduler.start_dockerizer') as mock_start:
            mock_start.return_value = True
            build_job, image_exists, build_status = dockerizer_scheduler.create_build_job(
                user=self.project.user,
                project=self.project,
                config=config,
                code_reference=self.code_reference
            )
        assert mock_start.call_count == 1
        assert image_exists is False
        assert build_status is True
        assert BuildJob.objects.count() == 2
