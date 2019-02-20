from unittest.mock import patch

import pytest

from django.test import override_settings

from constants.jobs import JobLifeCycle
from db.managers.deleted import ArchivedManager, LiveManager
from db.models.build_jobs import BuildJob, BuildJobStatus
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_code_reference import CodeReferenceFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.build_jobs_mark
class TestBuildJobModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.code_reference = CodeReferenceFactory()

    def test_build_job_creation_triggers_status_creation_mock(self):
        with patch.object(BuildJob, 'set_status') as mock_fct:
            BuildJobFactory()
        assert mock_fct.call_count == 1

    def test_build_job_creation_triggers_status_creation(self):
        job = BuildJobFactory()
        assert BuildJobStatus.objects.filter(job=job).count() == 1
        assert job.last_status == JobLifeCycle.CREATED

    def test_status_update_results_in_new_updated_at_datetime(self):
        job = BuildJobFactory()
        updated_at = job.updated_at
        # Create new status
        BuildJobStatus.objects.create(job=job, status=JobLifeCycle.BUILDING)
        job.refresh_from_db()
        assert updated_at < job.updated_at
        updated_at = job.updated_at
        # Create status Using set_status
        job.set_status(JobLifeCycle.RUNNING)
        job.refresh_from_db()
        assert updated_at < job.updated_at

    def test_create_build_job_from_experiment(self):
        assert BuildJobStatus.objects.count() == 0
        experiment = ExperimentFactory(project=self.project)

        build_job, rebuild = BuildJob.create(
            user=experiment.user,
            project=experiment.project,
            config=experiment.specification.build,
            configmap_refs=experiment.specification.configmap_refs,
            secret_refs=experiment.specification.secret_refs,
            code_reference=self.code_reference)

        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1

    def test_create_build_from_notebook(self):
        assert BuildJobStatus.objects.count() == 0
        notebook = NotebookJobFactory(project=self.project)
        build_job, rebuild = BuildJob.create(
            user=notebook.user,
            project=notebook.project,
            config=notebook.specification.build,
            configmap_refs=notebook.specification.configmap_refs,
            secret_refs=notebook.specification.secret_refs,
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1

    def test_create_build_with_same_config(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, False)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1
        assert new_build_job == build_job

    def test_create_build_with_same_config_and_force_create_new_build_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config and force creates a new build job
        new_build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference,
            nocache=True)
        self.assertEqual(rebuild, True)
        assert BuildJobStatus.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert new_build_job != build_job

        # Building with same config does not create a new build job
        new_build_job_v2, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, False)
        assert BuildJobStatus.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert new_build_job == new_build_job_v2

    def test_create_build_with_latest_tag_does_not_results_in_new_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:latest'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:latest'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, False)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1
        assert new_build_job == build_job

    @override_settings(BUILD_ALWAYS_PULL_LATEST=True)
    def test_create_build_with_latest_tag_and_always_pull_latest_creates_new_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:latest'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:latest'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert new_build_job != build_job

    def test_create_build_without_tag_always_doesn_not_create_new_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, False)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1
        assert new_build_job == build_job

    @override_settings(BUILD_ALWAYS_PULL_LATEST=True)
    def test_create_build_without_tag_and_rebuild_latest_always_results_in_new_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job, rebuild = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image'},
            code_reference=self.code_reference)
        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert new_build_job != build_job

    def test_build_job_statuses(self):
        assert BuildJobStatus.objects.count() == 0
        experiment = ExperimentFactory(project=self.project)

        build_job, rebuild = BuildJob.create(
            user=experiment.user,
            project=experiment.project,
            config=experiment.specification.build,
            configmap_refs=experiment.specification.configmap_refs,
            secret_refs=experiment.specification.secret_refs,
            code_reference=self.code_reference)

        self.assertEqual(rebuild, True)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        build_job.set_status(JobLifeCycle.FAILED)
        assert BuildJobStatus.objects.count() == 2
        build_job.set_status(JobLifeCycle.SUCCEEDED)
        assert BuildJobStatus.objects.count() == 2

    def test_managers(self):
        assert isinstance(BuildJob.objects, LiveManager)
        assert isinstance(BuildJob.archived, ArchivedManager)

    def test_archive(self):
        assert BuildJobStatus.objects.count() == 0
        experiment = ExperimentFactory(project=self.project)

        build_job, rebuild = BuildJob.create(
            user=experiment.user,
            project=experiment.project,
            config=experiment.specification.build,
            configmap_refs=experiment.specification.configmap_refs,
            secret_refs=experiment.specification.secret_refs,
            code_reference=self.code_reference)

        self.assertEqual(rebuild, True)
        assert build_job.deleted is False
        assert BuildJob.objects.count() == 1
        assert BuildJob.all.count() == 1

        build_job.archive()
        assert build_job.deleted is True
        assert BuildJob.objects.count() == 0
        assert BuildJob.all.count() == 1

        build_job.restore()
        assert build_job.deleted is False
        assert BuildJob.objects.count() == 1
        assert BuildJob.all.count() == 1
