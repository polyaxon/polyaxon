# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker
from polyaxon_schemas.experiment import ExperimentConfig

from polyaxon_client.experiment_group import ExperimentGroupClient

faker = Faker()


class TestExperimentGroupClient(TestCase):
    def setUp(self):
        self.client = ExperimentGroupClient(host='http://localhost',
                                            version='v1',
                                            reraise=True)
        self.base_url = ExperimentGroupClient.BASE_URL.format('http://localhost', 'v1')

    @httpretty.activate
    def test_list_experiments(self):
        group_uuid = uuid.uuid4().hex
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(name='xp',
                                uuid=xp_uuid,
                                project=project_uuid,
                                group=group_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.base_url,
                ExperimentGroupClient.ENDPOINT,
                group_uuid,
                'experiments'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_experiments(group_uuid)
        assert len(xps_results) == 10

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.base_url,
                ExperimentGroupClient.ENDPOINT,
                group_uuid,
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_experiments(group_uuid, page=2)
        assert len(xps_results) == 10
