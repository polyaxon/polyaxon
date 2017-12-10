# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase

import datetime
import httpretty
from faker import Faker
from polyaxon_schemas.experiment import ExperimentConfig, ExperimentStatusConfig, \
    ExperimentJobConfig, ExperimentJobStatusConfig

from polyaxon_client.experiment import ExperimentClient

faker = Faker()


class TestExperimentClient(TestCase):
    def setUp(self):
        self.client = ExperimentClient(host='http://localhost',
                                       version='v1',
                                       reraise=True)
        self.base_url = ExperimentClient.BASE_URL.format('http://localhost', 'v1')

    @httpretty.activate
    def test_list_experiments(self):
        experiments = [ExperimentConfig(faker.word).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT),
            body=json.dumps({'results': experiments, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        experiments = self.client.list_experiments()
        assert len(experiments) == 10

    @httpretty.activate
    def test_get_experiment(self):
        object = ExperimentConfig(faker.word()).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                'uuid'),
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_experiment('uuid')
        assert object == result.to_dict()

    @httpretty.activate
    def test_update_project(self):
        object = ExperimentConfig(faker.word())
        experiment_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.PATCH,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                experiment_uuid),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment(experiment_uuid, {'name': 'new'})
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_delete_experiment(self):
        experiment_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.DELETE,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                experiment_uuid),
            content_type='application/json',
            status=204)
        result = self.client.delete_experiment(experiment_uuid)
        assert result.status_code == 204

    @httpretty.activate
    def test_get_experiment_status(self):
        experiment_uuid = uuid.uuid4().hex
        object = ExperimentStatusConfig(uuid=experiment_uuid,
                                        experiment=experiment_uuid,
                                        created_at=datetime.datetime.now(),
                                        status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                'uuid',
                'status'),
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_status('uuid')
        assert object == result.to_dict()

    @httpretty.activate
    def test_list_experiment_jobs(self):
        experiment_uuid = uuid.uuid4().hex
        job_uuid = uuid.uuid4().hex
        xps = [ExperimentJobConfig(uuid=job_uuid,
                                   experiment=experiment_uuid,
                                   created_at=datetime.datetime.now(),
                                   definition='').to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                experiment_uuid,
                'jobs',
            ),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_jobs(experiment_uuid)
        assert len(xps_results) == 10

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                experiment_uuid,
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_jobs(experiment_uuid, page=2)
        assert len(xps_results) == 10

    @httpretty.activate
    def test_get_experiment_job_status(self):
        experiment_uuid = uuid.uuid4().hex
        job_uuid = uuid.uuid4().hex
        object = ExperimentJobStatusConfig(uuid=uuid.uuid4().hex,
                                           job=job_uuid,
                                           created_at=datetime.datetime.now(),
                                           status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                experiment_uuid,
                'jobs',
                job_uuid,
                'status'),
            body=json.dumps(object),
            content_type='application/json',
            status=200)
        result = self.client.get_job_status(experiment_uuid, job_uuid)
        assert object == result.to_dict()

    @httpretty.activate
    def test_restart_experiment(self):
        object = ExperimentConfig(name=faker.word())
        experimnt_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            ExperimentClient._build_url(
                self.base_url,
                ExperimentClient.ENDPOINT,
                experimnt_uuid,
                'restart'),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.restart(experimnt_uuid)
        assert result.to_dict() == object.to_dict()
