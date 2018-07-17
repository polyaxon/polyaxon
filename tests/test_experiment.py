# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.experiment import ExperimentClient
from polyaxon_schemas.experiment import (
    ExperimentConfig,
    ExperimentJobConfig,
    ExperimentMetricConfig,
    ExperimentStatusConfig
)

faker = Faker()


class TestExperimentClient(TestCase):
    def setUp(self):
        self.client = ExperimentClient(host='localhost',
                                       http_port=8000,
                                       ws_port=1337,
                                       version='v1',
                                       token=faker.uuid4(),
                                       reraise=True)

    @httpretty.activate
    def test_list_experiments(self):
        experiments = [ExperimentConfig(config={}).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'experiments'
            ),
            body=json.dumps({'results': experiments, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments()
        assert len(response['results']) == 10

    @httpretty.activate
    def test_get_experiment(self):
        exp = ExperimentConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1
            ),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)
        result = self.client.get_experiment('username', 'project_name', 1)
        assert exp == result.to_dict()

    @httpretty.activate
    def test_update_experiment(self):
        exp = ExperimentConfig(config={})
        httpretty.register_uri(
            httpretty.PATCH,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_delete_experiment(self):
        httpretty.register_uri(
            httpretty.DELETE,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1),
            content_type='application/json',
            status=204)
        result = self.client.delete_experiment('username', 'project_name', 1)
        assert result.status_code == 204

    @httpretty.activate
    def test_get_experiment_statuses_and_latest_code(self):
        exp = ExperimentStatusConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'statuses'),
            body=json.dumps({'results': [exp], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_get_experiment_metrics(self):
        exp = ExperimentMetricConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     values={'accuracy': 0.9}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'metrics'),
            body=json.dumps({'results': [exp], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_metrics('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_create_experiment_metric(self):
        exp = ExperimentMetricConfig(id=1,
                                     uuid=uuid.uuid4().hex,
                                     experiment=1,
                                     created_at=datetime.datetime.now(),
                                     values={'accuracy': 0.9}).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'metrics'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)
        response = self.client.create_metric('username', 'project_name', 1,
                                             values={'accuracy': 0.9})
        assert response.to_dict() == exp

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
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
            ),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_jobs('username', 'project_name', 1)
        assert len(response['results']) == 10

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'jobs') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_jobs('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10

    @httpretty.activate
    def test_restart_experiment(self):
        exp = ExperimentConfig(config={})
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'restart'),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.restart('username', 'project_name', 1)
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_resume_experiment_with_config(self):
        exp = ExperimentConfig(config={})
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'resume'),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.restart('username', 'project_name', 1, config, update_code=True)
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_resume_experiment(self):
        exp = ExperimentConfig(config={})
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'resume'),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.resume('username', 'project_name', 1)
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_resume_experiment_with_config(self):
        exp = ExperimentConfig(config={})
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'resume'),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.resume('username', 'project_name', 1, config)
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_copy_experiment(self):
        exp = ExperimentConfig(config={})
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'copy'),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.copy('username', 'project_name', 1)
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_copy_experiment_with_config(self):
        exp = ExperimentConfig(config={})
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'copy'),
            body=json.dumps(exp.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.copy('username', 'project_name', 1, config)
        assert result.to_dict() == exp.to_dict()

    @httpretty.activate
    def test_stop_experiment(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_experiment_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.client.logs('username', 'project_name', 1, stream=False)
        assert response.content.decode() == 'some text'

    @httpretty.activate
    def test_start_experiment_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'tensorboard',
                'start'),
            content_type='application/json',
            status=200)
        result = self.client.start_tensorboard('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_start_experiment_tensorboard_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'tensorboard',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.start_tensorboard('username', 'project_name', 1, obj)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_experiment_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'tensorboard',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop_tensorboard('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_bookmark_experiment(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.client.bookmark('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_unbookmark_experiment(self):
        httpretty.register_uri(
            httpretty.DELETE,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.client.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200
