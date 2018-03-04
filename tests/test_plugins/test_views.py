# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import mock

from unittest.mock import patch

from rest_framework import status

from factories.factory_repos import RepoFactory
from factories.fixtures import plugin_spec_parsed_content
from libs.views import ProtectedView
from plugins.models import TensorboardJob, NotebookJob
from polyaxon.urls import API_V1
from projects.models import Project
from factories.factory_projects import ProjectFactory
from spawner import K8SProjectSpawner, scheduler
from spawner.templates.constants import DEPLOYMENT_NAME
from tests.utils import BaseViewTest


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
        with patch('projects.tasks.start_tensorboard.delay') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1
        self.object.refresh_from_db()
        assert isinstance(self.object.tensorboard, TensorboardJob)

    def test_spawner_start(self):
        assert self.queryset.count() == 1
        with patch('spawner.scheduler.start_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_start_with_updated_config(self):
        with patch('projects.tasks.start_tensorboard.delay') as _:
            self.auth_client.post(self.url)
        # Start with default config
        self.object.refresh_from_db()
        config = self.object.tensorboard.config

        # Simulate stop the tensorboard
        self.object.has_tensorboard = False
        self.object.save()

        # Starting the tensorboard without config should pass
        with patch('projects.tasks.start_tensorboard.delay') as _:
            self.auth_client.post(self.url)
        # Check that still using same config
        self.object.tensorboard.refresh_from_db()
        assert config == self.object.tensorboard.config

        # Simulate stop the tensorboard
        self.object.has_tensorboard = False
        self.object.save()

        # Starting again the tensorboard with different config
        with patch('projects.tasks.start_tensorboard.delay') as _:
            self.auth_client.post(self.url,
                                  data={'config': plugin_spec_parsed_content.parsed_data})

        self.object.tensorboard.refresh_from_db()
        # Check that the image was update
        assert config != self.object.tensorboard.config


class TestStopTensorboardViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user, has_tensorboard=True)
        self.url = '/{}/{}/{}/tensorboard/stop'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('projects.tasks.stop_tensorboard.delay') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('spawner.scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


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
        data = {'config': plugin_spec_parsed_content.parsed_data}
        assert self.queryset.count() == 1
        assert self.object.notebook is None
        with patch('projects.tasks.build_notebook.delay') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1
        self.object.refresh_from_db()
        assert isinstance(self.object.notebook, NotebookJob)

    def test_start(self):
        data = {'config': plugin_spec_parsed_content.parsed_data}
        assert self.queryset.count() == 1
        with patch('dockerizer.builders.notebooks.build_notebook_job') as build_mock_fct:
            with patch('projects.tasks.start_notebook.delay') as mock_fct:
                resp = self.auth_client.post(self.url, data)
        assert build_mock_fct.call_count == 1
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_build_with_updated_config(self):
        data = {'config': plugin_spec_parsed_content.parsed_data}
        with patch('projects.tasks.build_notebook.delay') as _:
            self.auth_client.post(self.url, data)
        # Start with default config
        self.object.refresh_from_db()
        config = self.object.notebook.config

        # Simulate stop the notebook
        self.object.has_notebook = False
        self.object.save()

        # Starting the notebook without config should pass
        with patch('projects.tasks.build_notebook.delay') as _:
            self.auth_client.post(self.url)
        # Check that still using same config
        self.object.notebook.refresh_from_db()
        assert config == self.object.notebook.config

        # Simulate stop the notebook
        self.object.has_notebook = False
        self.object.save()

        # Starting again the notebook with different config
        data['config']['run']['image'] = 'image_v2'
        with patch('projects.tasks.build_notebook.delay') as _:
            self.auth_client.post(self.url, data)

        self.object.notebook.refresh_from_db()
        # Check that the image was update
        assert config != self.object.notebook.config


class TestStopNotebookViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user, has_notebook=True)
        RepoFactory(project=self.object)
        self.url = '/{}/{}/{}/notebook/stop'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('projects.tasks.stop_notebook.delay') as mock_fct:
            with patch('repos.git.commit') as mock_git_commit:
                resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_stop_without_committing(self):
        data = {'commit': False}
        assert self.queryset.count() == 1
        with patch('projects.tasks.stop_notebook.delay') as mock_fct:
            with patch('repos.git.commit') as mock_git_commit:
                resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('spawner.scheduler.stop_notebook') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


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
        return K8SProjectSpawner._get_proxy_url(
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
    plugin_app = K8SProjectSpawner.TENSORBOARD_APP

    def test_project_requests_tensorboard_url(self):
        project = ProjectFactory(user=self.auth_client.user, has_tensorboard=True)
        with patch('spawner.scheduler.get_tensorboard_url') as mock_fct:
            response = self.auth_client.get(self._get_url(project))

        assert mock_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('spawner.scheduler.K8SProjectSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user, has_tensorboard=True)
        deployment_name = DEPLOYMENT_NAME.format(
            project_uuid=project.uuid.hex, name=self.plugin_app)
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/'.format(service_url)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('spawner.scheduler.K8SProjectSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user, has_tensorboard=True)
        deployment_name = DEPLOYMENT_NAME.format(
            project_uuid=project.uuid.hex, name=self.plugin_app)
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


class TestNotebookViewV1(BaseTestPluginViewV1):
    plugin_app = K8SProjectSpawner.NOTEBOOK_APP

    def test_project_requests_notebook_url(self):
        project = ProjectFactory(user=self.auth_client.user, has_notebook=True)
        with patch('spawner.scheduler.get_notebook_url') as mock_url_fct:
            with patch('spawner.scheduler.get_notebook_token') as mock_token_fct:
                response = self.auth_client.get(self._get_url(project))

        assert mock_url_fct.call_count == 1
        assert mock_token_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('spawner.scheduler.K8SProjectSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user, has_notebook=True)
        deployment_name = DEPLOYMENT_NAME.format(
            project_uuid=project.uuid.hex, name=self.plugin_app)
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_notebook_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}?token={}'.format(
            service_url,
            'tree',
            scheduler.get_notebook_token(project)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('spawner.scheduler.K8SProjectSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user, has_notebook=True)
        deployment_name = DEPLOYMENT_NAME.format(
            project_uuid=project.uuid.hex, name=self.plugin_app)
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
            scheduler.get_notebook_token(project)
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
            scheduler.get_notebook_token(project)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


# Prevent this base class from running tests
del BaseTestPluginViewV1
