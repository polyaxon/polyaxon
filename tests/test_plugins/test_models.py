import pytest
from mock import patch

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import MULTIPART_CONTENT

from constants.jobs import JobLifeCycle
from db.models.plugins import NotebookJob, NotebookJobStatus, TensorboardJob, TensorboardJobStatus
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from polyaxon.urls import API_V1
from tests.utils import BaseTest, BaseViewTest


@pytest.mark.plugins
class TestPluginsModel(BaseTest):
    def test_project_deletion_cascade_to_tensorboard_job(self):
        assert TensorboardJob.objects.count() == 0
        project = ProjectFactory()
        TensorboardJobFactory(project=project)
        assert TensorboardJob.objects.count() == 1

        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as _:  # noqa
            with patch('scheduler.notebook_scheduler.stop_notebook') as _:  # noqa
                project.delete()
        assert TensorboardJob.objects.count() == 0

    def test_project_deletion_cascade_to_notebook_job(self):
        assert NotebookJob.objects.count() == 0
        project = ProjectFactory()
        NotebookJobFactory(project=project)
        assert NotebookJob.objects.count() == 1

        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as _:  # noqa
            with patch('scheduler.notebook_scheduler.stop_notebook') as _:  # noqa
                project.delete()
        assert NotebookJob.objects.count() == 0

    def test_tensorboard_creation_triggers_status_creation(self):
        assert TensorboardJobStatus.objects.count() == 0
        project = ProjectFactory()
        TensorboardJobFactory(project=project)

        assert TensorboardJobStatus.objects.count() == 1
        assert project.tensorboard.last_status == JobLifeCycle.CREATED

    def test_notebook_creation_triggers_status_creation(self):
        assert NotebookJobStatus.objects.count() == 0
        project = ProjectFactory()
        NotebookJobFactory(project=project)

        assert NotebookJobStatus.objects.count() == 1
        assert project.notebook.last_status == JobLifeCycle.CREATED


@pytest.mark.plugins
class TestPluginJobCommit(BaseViewTest):
    factory_class = None

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

    def test_plugin_job_is_saved_with_commit(self):
        uploaded_file = self.get_upload_file()

        self.auth_client.put(self.url,
                             data={'repo': uploaded_file},
                             content_type=MULTIPART_CONTENT)

        last_commit = self.project.repo.last_commit
        assert last_commit is not None

        # Check plugin job is created with commit
        plugin_job = self.factory_class(project=self.project)  # pylint:disable=not-callable

        assert plugin_job.code_reference.commit == last_commit[0]
        assert plugin_job.code_reference.repo == self.project.repo

        # Make a new upload with repo_new.tar.gz containing 2 files
        new_uploaded_file = self.get_upload_file('updated_repo')
        self.auth_client.put(self.url,
                             data={'repo': new_uploaded_file},
                             content_type=MULTIPART_CONTENT)

        new_commit = self.project.repo.last_commit
        assert new_commit is not None
        assert new_commit[0] != last_commit[0]

        # Check new plugin job is created with new commit
        new_plugin_job = self.factory_class(project=self.project)  # pylint:disable=not-callable
        assert new_plugin_job.code_reference.commit == new_commit[0]
        assert new_plugin_job.code_reference.repo == self.project.repo


@pytest.mark.plugins
class TestTensorboardCommit(TestPluginJobCommit):
    factory_class = TensorboardJobFactory


@pytest.mark.plugins
class TestNotebookCommit(TestPluginJobCommit):
    factory_class = NotebookJobFactory


del TestPluginJobCommit
