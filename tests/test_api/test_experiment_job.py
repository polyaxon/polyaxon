# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.experiment_job import ExperimentJobApi
from polyaxon_client.schemas import ExperimentJobConfig, ExperimentJobStatusConfig


class TestExperimentJobClient(TestBaseApi):

    def setUp(self):
        super(TestExperimentJobClient, self).setUp()
        self.api_handler = ExperimentJobApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_job(self):
        obj = ExperimentJobConfig(uuid=uuid.uuid4().hex,
                                  experiment=1,
                                  created_at=datetime.datetime.now(),
                                  updated_at=datetime.datetime.now(),
                                  definition={}).to_dict()
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
                'uuid'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.api_handler.get_job('username', 'project_name', 1, 'uuid')
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
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
        response = self.api_handler.get_statuses('username', 'project_name', 1, 1)
        assert len(response['results']) == 1
