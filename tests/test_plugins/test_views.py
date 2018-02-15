# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest.mock import patch

from rest_framework import status

from factories.fixtures import tensorboard_spec_parsed_content
from plugins.models import TensorboardJob
from polyaxon.urls import API_V1
from projects.models import Project
from factories.factory_projects import ProjectFactory
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
                                  data={'config': tensorboard_spec_parsed_content.parsed_data})

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

    def test_spawner_start(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('spawner.scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1
