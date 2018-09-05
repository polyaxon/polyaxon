# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import json
import uuid
from collections import Mapping

import httpretty
from polyaxon_schemas.code_reference import CodeReferenceConfig

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.experiment import ExperimentApi
from polyaxon_client.schemas import (
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentMetricConfig,
    ExperimentStatusConfig
)
from tests.test_api.utils import TestBaseApi


class TestExperimentApi(TestBaseApi):

    def setUp(self):
        super(TestExperimentApi, self).setUp()
        self.api_handler = ExperimentApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_list_experiments(self):
        experiments = [ExperimentConfig(config={}).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'experiments'
            ),
            body=json.dumps({'results': experiments, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.list_experiments()
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], ExperimentConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.list_experiments()
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_get_experiment(self):
        exp = ExperimentConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1
            ),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.get_experiment('username', 'project_name', 1)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_experiment('username', 'project_name', 1)
        assert result == exp

    @httpretty.activate
    def test_update_experiment(self):
        exp = ExperimentConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.PATCH,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.update_experiment('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.update_experiment('username', 'project_name', 1, {'name': 'new'})
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.update_experiment(
                'username', 'project_name', 1, {'name': 'new'}, background=True),
            method='patch')

    @httpretty.activate
    def test_delete_experiment(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1),
            content_type='application/json',
            status=204)
        result = self.api_handler.delete_experiment('username', 'project_name', 1)
        assert result.status_code == 204

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.delete_experiment(
                'username', 'project_name', 1, background=True),
            method='delete')

    @httpretty.activate
    def test_get_experiment_statuses_and_latest_code(self):
        exp = ExperimentStatusConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'statuses'),
            body=json.dumps({'results': [exp], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], ExperimentStatusConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_create_experiment_status(self):
        exp = ExperimentStatusConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     status='Running').to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
    def test_create_experiment_code_reference(self):
        coderef = CodeReferenceConfig(commit='3783ab36703b14b91b15736fe4302bfb8d52af1c',
                                      head='3783ab36703b14b91b15736fe4302bfb8d52af1c',
                                      branch='feature1',
                                      git_url='https://bitbucket.org:foo/bar.git',
                                      is_dirty=True).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'coderef'),
            body=json.dumps(coderef),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.create_code_reference(
            'username', 'project_name', 1, coderef=coderef)
        assert response.to_dict() == coderef

        # Raw response
        self.set_raw_response()
        response = self.api_handler.create_code_reference(
            'username', 'project_name', 1, coderef=coderef)
        assert response == coderef

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.create_code_reference(
                'username', 'project_name', 1, coderef=coderef, background=True),
            method='post')

    @httpretty.activate
    def test_get_experiment_metrics(self):
        exp = ExperimentMetricConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     values={'accuracy': 0.9}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'metrics'),
            body=json.dumps({'results': [exp], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.get_metrics('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], ExperimentMetricConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.get_metrics('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_create_experiment_metric(self):
        exp = ExperimentMetricConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     values={'accuracy': 0.9}).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'metrics'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.create_metric('username', 'project_name', 1,
                                                  values={'accuracy': 0.9})
        assert response.to_dict() == exp

        # Raw response
        self.set_raw_response()
        response = self.api_handler.create_metric('username', 'project_name', 1,
                                                  values={'accuracy': 0.9})
        assert response == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.create_metric(
                'username', 'project_name', 1, values={'accuracy': 0.9}, background=True),
            method='post')

    @httpretty.activate
    def test_list_experiment_jobs(self):
        job_uuid = uuid.uuid4().hex
        xps = [ExperimentJobConfig(uuid=job_uuid,
                                   experiment=1,
                                   created_at=datetime.datetime.now(),
                                   updated_at=datetime.datetime.now(),
                                   definition={}).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
            ),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.list_jobs('username', 'project_name', 1)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], ExperimentJobConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.list_jobs('username', 'project_name', 1)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], Mapping)

        # Pagination
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'jobs') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        self.set_schema_response()
        response = self.api_handler.list_jobs('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], ExperimentJobConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.list_jobs('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_restart_experiment(self):
        exp = ExperimentConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'restart'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.restart('username', 'project_name', 1)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.restart('username', 'project_name', 1)
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.restart(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_restart_experiment_with_config(self):
        exp = ExperimentConfig(config={}).to_dict()
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'restart'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.restart('username', 'project_name', 1, config, update_code=True)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.restart('username', 'project_name', 1, config, update_code=True)
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.restart(
                'username', 'project_name', 1, config, background=True),
            method='post')

    @httpretty.activate
    def test_resume_experiment(self):
        exp = ExperimentConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'resume'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.resume('username', 'project_name', 1)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.resume('username', 'project_name', 1)
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.resume(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_resume_experiment_with_config(self):
        exp = ExperimentConfig(config={}).to_dict()
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'resume'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.resume('username', 'project_name', 1, config)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.resume('username', 'project_name', 1, config)
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.resume(
                'username', 'project_name', 1, config, background=True),
            method='post')

    @httpretty.activate
    def test_copy_experiment(self):
        exp = ExperimentConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'copy'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.copy('username', 'project_name', 1)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.copy('username', 'project_name', 1)
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.copy(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_copy_experiment_with_config(self):
        exp = ExperimentConfig(config={}).to_dict()
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'copy'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.copy('username', 'project_name', 1, config)
        assert result.to_dict() == exp

        # Raw response
        self.set_raw_response()
        result = self.api_handler.copy('username', 'project_name', 1, config)
        assert result == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.copy(
                'username', 'project_name', 1, config, background=True),
            method='post')

    @httpretty.activate
    def test_stop_experiment(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
    def test_experiment_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.api_handler.logs('username', 'project_name', 1, stream=False)
        assert response.content.decode() == 'some text'

    @httpretty.activate
    def test_start_experiment_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
    def test_start_experiment_tensorboard_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
    def test_stop_experiment_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
    def test_unbookmark_experiment(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
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
