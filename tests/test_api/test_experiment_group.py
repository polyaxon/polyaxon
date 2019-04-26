# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from collections import Mapping

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.experiment_group import ExperimentGroupApi
from polyaxon_client.schemas import ExperimentConfig, GroupConfig, GroupStatusConfig


class TestExperimentGroupApi(TestBaseApi):

    def setUp(self):
        super(TestExperimentGroupApi, self).setUp()
        self.api_handler = ExperimentGroupApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_experiment_group(self):
        obj = GroupConfig(content='text',
                          uuid=uuid.uuid4().hex,
                          project=uuid.uuid4().hex).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.get_experiment_group('username', 'project_name', 1)
        assert obj == result.to_dict()

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_experiment_group('username', 'project_name', 1)
        assert obj == result

    @httpretty.activate
    def test_list_experiments(self):
        group_uuid = uuid.uuid4().hex
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(uuid=xp_uuid,
                                project=project_uuid,
                                experiment_group=group_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments') + '?group=1',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.list_experiments('username', 'project_name', 1)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], ExperimentConfig)
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

        # Raw response
        self.set_raw_response()
        response = self.api_handler.list_experiments('username', 'project_name', 1)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], Mapping)
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

        # Pagination
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments') + '?group=1&offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        self.set_schema_response()
        response = self.api_handler.list_experiments('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], ExperimentConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.list_experiments('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], Mapping)

        # Query, Sort
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments') + '?group=1&query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        self.set_schema_response()
        response = self.api_handler.list_experiments('username',
                                                     'project_name',
                                                     1,
                                                     query='started_at:>=2010-10-10',
                                                     sort='created_at')
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], ExperimentConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.list_experiments('username',
                                                     'project_name',
                                                     1,
                                                     query='started_at:>=2010-10-10',
                                                     sort='created_at')
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_update_experiment_group(self):
        obj = GroupConfig(content='text',
                          uuid=uuid.uuid4().hex,
                          project=uuid.uuid4().hex).to_dict()
        httpretty.register_uri(
            httpretty.PATCH,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.update_experiment_group(
            'username', 'project_name', 1, {'content': 'new'})
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.update_experiment_group(
            'username', 'project_name', 1, {'content': 'new'})
        assert result == obj

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.update_experiment_group(
                'username', 'project_name', 1, {'content': 'new'}, background=True),
            method='patch')

    @httpretty.activate
    def test_delete_experiment_group(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1),
            content_type='application/json',
            status=204)
        result = self.api_handler.delete_experiment_group('username', 'project_name', 1)
        assert result.status_code == 204

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.delete_experiment_group(
                'username', 'project_name', 1, background=True),
            method='delete')

    @httpretty.activate
    def test_get_experiment_group_statuses(self):
        group = GroupStatusConfig(id=1,
                                  uuid=uuid.uuid4().hex,
                                  experiment_group=1,
                                  created_at=datetime.datetime.now(),
                                  status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'statuses'),
            body=json.dumps({'results': [group], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], GroupStatusConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_create_experiment_status(self):
        exp = GroupStatusConfig(id=1,
                                uuid=uuid.uuid4().hex,
                                experiment_group=1,
                                created_at=datetime.datetime.now(),
                                status='Running').to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'statuses'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.create_status('username', 'project_name', 1, status='running')
        assert response.to_dict() == exp

        # Raw response
        self.set_raw_response()
        response = self.api_handler.create_status('username', 'project_name', 1, status='running')
        assert response == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.create_status(
                'username', 'project_name', 1, status='running', background=True),
            method='post')

    @httpretty.activate
    def test_stop_experiment_group_all(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.stop(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_stop_experiment_group_pending(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop('username', 'project_name', 1, pending=True)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.stop(
                'username', 'project_name', 1, pending=True, background=True),
            method='post')

    @httpretty.activate
    def test_start_experiment_group_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'tensorboard',
                'start'),
            content_type='application/json',
            status=200)
        result = self.api_handler.start_tensorboard('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.start_tensorboard(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_start_experiment_group_tensorboard_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'tensorboard',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.api_handler.start_tensorboard('username', 'project_name', 1, obj)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.start_tensorboard(
                'username', 'project_name', 1, obj, background=True),
            method='post')

    @httpretty.activate
    def test_stop_experiment_group_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'tensorboard',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop_tensorboard('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.stop_tensorboard(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_bookmark_experiment(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.bookmark('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.bookmark(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_unbookmark_experiment_group(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'groups',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.unbookmark(
                'username', 'project_name', 1, background=True),
            method='delete')
