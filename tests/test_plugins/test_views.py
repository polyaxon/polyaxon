from unittest.mock import patch

import mock
import pytest

from rest_framework import status

from api.utils.views import ProtectedView
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.notebooks import NotebookJob, NotebookJobStatus
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus
from dockerizer.tasks import build_project_notebook
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from factories.fixtures import notebook_spec_parsed_content, tensorboard_spec_parsed_content
from scheduler import notebook_scheduler
from scheduler.spawners.notebook_spawner import NotebookSpawner
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates.constants import DEPLOYMENT_NAME
from scheduler.spawners.tensorboard_spawner import TensorboardSpawner
from tests.utils import BaseViewTest


@pytest.mark.plugins_mark
class TestStartTensorboardViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/{}/{}/tensorboard/start'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_start(self):
        assert self.queryset.count() == 1
        assert self.object.tensorboard is None
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        self.object.refresh_from_db()
        assert isinstance(self.object.tensorboard, TensorboardJob)

    def test_spawner_start(self):
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.start_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1

    def test_start_with_updated_config(self):
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Start with default config
        self.object.refresh_from_db()
        config = self.object.tensorboard.config

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()

        # Starting the tensorboard without config should pass
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Check that still using same config
        self.object.refresh_from_db()
        assert config == self.object.tensorboard.config

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()
        self.object.save()

        # Starting again the tensorboard with different config
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'config': tensorboard_spec_parsed_content.parsed_data})

        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        self.object.refresh_from_db()
        # Check that the image was update
        assert config != self.object.tensorboard.config

        # Trying to start an already running job returns 200
        # Starting again the tensorboard with different config
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'config': tensorboard_spec_parsed_content.parsed_data})

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_200_OK

    def test_start_during_build_process(self):
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED

        # Check that user cannot start a new job if it's already building
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        assert start_mock.call_count == 0

    def test_starting_stopping_tensorboard_creating_new_one_create_new_job(self):
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        self.object.tensorboard.set_status(status=JobLifeCycle.STOPPED)
        assert TensorboardJob.objects.count() == 1
        assert TensorboardJobStatus.objects.count() == 2

        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        assert TensorboardJob.objects.count() == 2
        assert TensorboardJobStatus.objects.count() == 3


@pytest.mark.plugins_mark
class TestStopTensorboardViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=self.object)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        self.url = '/{}/{}/{}/tensorboard/stop'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = TensorboardJob.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.tensorboards.'
                   'projects_tensorboard_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class TestStartNotebookViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/{}/{}/notebook/start'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_post_without_config_fails(self):
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_build(self):
        data = {'config': notebook_spec_parsed_content.parsed_data}
        assert self.queryset.count() == 1
        assert self.object.notebook is None
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        self.object.refresh_from_db()
        assert isinstance(self.object.notebook, NotebookJob)

    def test_start(self):
        data = {'config': notebook_spec_parsed_content.parsed_data}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_build.apply_async') as build_mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert build_mock_fct.call_count == 1

        # Simulate build
        with patch('dockerizer.builders.notebooks.build_notebook_job') as mock_fct:
            build_project_notebook(project_id=self.object.id)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1

    def test_build_with_updated_config(self):
        data = {'config': notebook_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Start with default config
        self.object.refresh_from_db()
        config = self.object.notebook.config

        # Simulate stop the notebook
        self.object.notebook.delete()

        # Starting the notebook without config should not pass
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        # Check that still using same config
        self.object.refresh_from_db()
        assert self.object.notebook is None

        # Starting again the notebook with different config
        data['config']['build']['image'] = 'image_v2'
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as _:  # noqa
            self.auth_client.post(self.url, data)

        self.object.refresh_from_db()
        # Check that the image was update
        assert config != self.object.notebook.config

        # Trying to start an already running job returns 200
        # Starting again the tensorboard with different config
        self.object.notebook.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data=data)

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_200_OK

    def test_start_during_build_process(self):
        data = {'config': notebook_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            resp = self.auth_client.post(self.url, data=data)

        assert resp.status_code == status.HTTP_201_CREATED
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.notebook.last_status == JobLifeCycle.CREATED

        # Check that user cannot start a new job if it's already building
        self.object.notebook.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            resp = self.auth_client.post(self.url)

        assert resp.status_code == status.HTTP_200_OK
        assert start_mock.call_count == 0

    def test_starting_stopping_notebook_creating_new_one_create_new_job(self):
        data = {'config': notebook_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            self.auth_client.post(self.url, data=data)

        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.notebook.last_status == JobLifeCycle.CREATED
        self.object.notebook.set_status(status=JobLifeCycle.STOPPED)
        assert NotebookJob.objects.count() == 1
        assert NotebookJobStatus.objects.count() == 2

        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            self.auth_client.post(self.url, data=data)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.notebook.last_status == JobLifeCycle.CREATED
        assert NotebookJob.objects.count() == 2
        assert NotebookJobStatus.objects.count() == 3


@pytest.mark.plugins_mark
class TestStopNotebookViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        tensorboard = NotebookJobFactory(project=self.object)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        RepoFactory(project=self.object)
        self.url = '/{}/{}/{}/notebook/stop'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async') as mock_fct:
            with patch('libs.repos.git.commit') as mock_git_commit:
                with patch('libs.repos.git.undo') as mock_git_undo:
                    resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 1
        assert mock_git_undo.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_stop_without_committing(self):
        data = {'commit': False}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async') as mock_fct:
            with patch('libs.repos.git.commit') as mock_git_commit:
                with patch('libs.repos.git.undo') as mock_git_undo:
                    resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 0
        assert mock_git_undo.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.notebook_scheduler.stop_notebook') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class BaseTestPluginViewV1(BaseViewTest):
    plugin_app = ''

    @classmethod
    def _get_url(cls, project, path=None):
        url = '/{}/{}/{}'.format(
            cls.plugin_app,
            project.user.username,
            project.name)

        if path:
            url = '{}/{}'.format(url, path)
        return url

    @classmethod
    def _get_service_url(cls, deployment_name):
        return ProjectJobSpawner._get_proxy_url(  # pylint:disable=protected-access
            namespace='polyaxon',
            job_name=cls.plugin_app,
            deployment_name=deployment_name,
            port=12503)

    def test_rejects_anonymous_user_and_redirected_to_login_page(self):
        project = ProjectFactory()
        response = self.client.get(self._get_url(project))
        assert response.status_code == 302

    def test_rejects_user_with_no_privileges(self):
        project = ProjectFactory(is_public=False)
        response = self.auth_client.get(self._get_url(project))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_project_with_no_job(self):
        project = ProjectFactory(user=self.auth_client.user)
        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestTensorboardViewV1(BaseTestPluginViewV1):
    plugin_app = TensorboardSpawner.TENSORBOARD_JOB_NAME

    def test_project_requests_tensorboard_url(self):
        project = ProjectFactory(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=project)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        with patch('scheduler.tensorboard_scheduler.get_tensorboard_url') as mock_fct:
            response = self.auth_client.get(self._get_url(project))

        assert mock_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=project)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = DEPLOYMENT_NAME.format(
            job_uuid=tensorboard.uuid.hex, name=self.plugin_app)
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/'.format(service_url)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=project)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = DEPLOYMENT_NAME.format(
            job_uuid=tensorboard.uuid.hex, name=self.plugin_app)
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        # To `tree?`
        response = self.auth_client.get(self._get_url(project, 'tree?'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'tree/'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

        # To static files
        response = self.auth_client.get(
            self._get_url(project, 'static/components/something?v=4.7.0'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'static/components/something?v=4.7.0'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


@pytest.mark.plugins_mark
class TestNotebookViewV1(BaseTestPluginViewV1):
    plugin_app = NotebookSpawner.NOTEBOOK_JOB_NAME

    def test_project_requests_notebook_url(self):
        project = ProjectFactory(user=self.auth_client.user)
        notebook = NotebookJobFactory(project=project)
        notebook.set_status(status=JobLifeCycle.RUNNING)
        with patch('scheduler.notebook_scheduler.get_notebook_url') as mock_url_fct:
            with patch('scheduler.notebook_scheduler.get_notebook_token') as mock_token_fct:
                response = self.auth_client.get(self._get_url(project))

        assert mock_url_fct.call_count == 1
        assert mock_token_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('scheduler.notebook_scheduler.NotebookSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        notebook = NotebookJobFactory(project=project)
        notebook.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = DEPLOYMENT_NAME.format(
            job_uuid=notebook.uuid.hex, name=self.plugin_app)
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_notebook_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}?token={}'.format(
            service_url,
            'tree',
            notebook_scheduler.get_notebook_token(notebook)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('scheduler.notebook_scheduler.NotebookSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        notebook = NotebookJobFactory(project=project)
        notebook.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = DEPLOYMENT_NAME.format(
            job_uuid=notebook.uuid.hex, name=self.plugin_app)
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_notebook_url.return_value = service_url

        # To `tree?`
        response = self.auth_client.get(self._get_url(project, 'tree?'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}?token={}'.format(
            service_url,
            'tree',
            notebook_scheduler.get_notebook_token(notebook)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

        # To static files
        response = self.auth_client.get(
            self._get_url(project, 'static/components/something?v=4.7.0'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}&token={}'.format(
            service_url,
            'static/components/something?v=4.7.0',
            notebook_scheduler.get_notebook_token(notebook)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


# Prevent this base class from running tests
del BaseTestPluginViewV1
