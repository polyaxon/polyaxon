# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase

import datetime
import httpretty
from faker import Faker
from polyaxon_schemas.experiment import (
    ExperimentConfig,
    ExperimentStatusConfig,
    ExperimentJobConfig,
    ExperimentMetricConfig)

from polyaxon_client.experiment import ExperimentClient

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
        object = ExperimentConfig(config={}).to_dict()
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
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_experiment('username', 'project_name', 1)
        assert object == result.to_dict()

    @httpretty.activate
    def test_update_project(self):
        object = ExperimentConfig(config={})
        httpretty.register_uri(
            httpretty.PATCH,
            ExperimentClient._build_url(
                self.client.base_url,
                ExperimentClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == object.to_dict()

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
    def test_get_experiment_statuses(self):
        experiment_uuid = uuid.uuid4().hex
        object = ExperimentStatusConfig(uuid=experiment_uuid,
                                        experiment=experiment_uuid,
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
            body=json.dumps({'results': [object], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_get_experiment_metrics(self):
        experiment_uuid = uuid.uuid4().hex
        object = ExperimentMetricConfig(uuid=experiment_uuid,
                                        experiment=experiment_uuid,
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
            body=json.dumps({'results': [object], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_metrics('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_create_experiment_metric(self):
        experiment_uuid = uuid.uuid4().hex
        object = ExperimentMetricConfig(uuid=experiment_uuid,
                                        experiment=experiment_uuid,
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
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        response = self.client.create_metric('username', 'project_name', 1,
                                             values={'accuracy': 0.9})
        assert response.to_dict() == object

    @httpretty.activate
    def test_list_experiment_jobs(self):
        experiment_uuid = uuid.uuid4().hex
        job_uuid = uuid.uuid4().hex
        xps = [ExperimentJobConfig(uuid=job_uuid,
                                   experiment=experiment_uuid,
                                   experiment_name='user.project.1',
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
        object = ExperimentConfig(config={})
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
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.restart('username', 'project_name', 1)
        assert result.to_dict() == object.to_dict()

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
