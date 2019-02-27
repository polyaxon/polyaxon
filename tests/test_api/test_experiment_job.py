# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from collections import Mapping

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
            BaseApiHandler.build_url(
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

        # Schema response
        result = self.api_handler.get_job('username', 'project_name', 1, 'uuid')
        assert result.to_dict() == obj

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_job('username', 'project_name', 1, 'uuid')
        assert result == obj

    @httpretty.activate
    def test_get_experiment_job_status(self):
        obj = ExperimentJobStatusConfig(id=1,
                                        uuid=uuid.uuid4().hex,
                                        job=1,
                                        created_at=datetime.datetime.now(),
                                        status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
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

        # Schema response
        response = self.api_handler.get_statuses('username', 'project_name', 1, 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], ExperimentJobStatusConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.get_statuses('username', 'project_name', 1, 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_experiment_job_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments',
                1,
                'jobs',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.api_handler.logs('username', 'project_name', 1, 1, stream=False)
        assert response.content.decode() == 'some text'
