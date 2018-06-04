import pytest

from constants.jobs import JobLifeCycle
from db.models.build_jobs import BuildJob, BuildJobStatus
from factories.code_reference import CodeReferenceFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseTest


@pytest.mark.build_jobs_mark
class TestBuildJobModels(BaseTest):
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.code_reference = CodeReferenceFactory()

    def test_create_build_job_from_experiment(self):
        assert BuildJobStatus.objects.count() == 0
        experiment = ExperimentFactory(project=self.project)

        build_job = BuildJob.create(
            user=experiment.user,
            project=experiment.project,
            config=experiment.specification.run_exec,
            code_reference=self.code_reference)

        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1

    def test_create_build_from_notebook(self):
        assert BuildJobStatus.objects.count() == 0
        notebook = NotebookJobFactory(project=self.project)
        build_job = BuildJob.create(
            user=notebook.user,
            project=notebook.project,
            config=notebook.specification.run_exec,
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1

    def test_create_build_with_same_config(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:test'},
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1
        assert new_build_job == build_job

    def test_create_build_with_latest_tag_always_results_in_new_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:latest'},
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image:latest'},
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert new_build_job != build_job

    def test_create_build_without_tag_always_results_in_new_job(self):
        assert BuildJobStatus.objects.count() == 0
        assert BuildJob.objects.count() == 0
        build_job = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image'},
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 1
        assert BuildJob.objects.count() == 1

        # Building with same config does not create a new build job
        new_build_job = BuildJob.create(
            user=self.project.user,
            project=self.project,
            config={'image': 'my_image'},
            code_reference=self.code_reference)
        assert build_job.last_status == JobLifeCycle.CREATED
        assert BuildJobStatus.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert new_build_job != build_job
