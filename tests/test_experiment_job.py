# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.experiment_job import ExperimentJobClient
from polyaxon_schemas.experiment import ExperimentJobConfig, ExperimentJobStatusConfig

faker = Faker()


class TestExperimentJobClient(TestCase):
    def setUp(self):
        self.client = ExperimentJobClient(host='localhost',
                                          http_port=8000,
                                          ws_port=1337,
                                          version='v1',
                                          token=faker.uuid4(),
                                          reraise=True)

    @httpretty.activate
    def test_get_job(self):
        obj = ExperimentJobConfig(uuid=uuid.uuid4().hex,
                                  experiment=1,
                                  created_at=datetime.datetime.now(),
                                  updated_at=datetime.datetime.now(),
                                  definition={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentJobClient._build_url(
                self.client.base_url,
                ExperimentJobClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
                'uuid'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.get_job('username', 'project_name', 1, 'uuid')
        assert obj == result.to_dict()

    @httpretty.activate
    def test_get_experiment_job_status(self):
        obj = ExperimentJobStatusConfig(id=1,
                                        uuid=uuid.uuid4().hex,
                                        job=1,
                                        created_at=datetime.datetime.now(),
                                        status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentJobClient._build_url(
                self.client.base_url,
                ExperimentJobClient.ENDPOINT,
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
                1,
                'statuses'),
            body=json.dumps({'results': [obj], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1, 1)
        assert len(response['results']) == 1
