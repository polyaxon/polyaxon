# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig

from polyaxon_client.experiment_group import ExperimentGroupClient

faker = Faker()


class TestExperimentGroupClient(TestCase):
    def setUp(self):
        self.client = ExperimentGroupClient(host='localhost',
                                            http_port=8000,
                                            ws_port=1337,
                                            version='v1',
                                            token=faker.uuid4(),
                                            reraise=True)

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
                self.client.base_url,
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
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                group_uuid,
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_experiments(group_uuid, page=2)
        assert len(xps_results) == 10

    @httpretty.activate
    def test_update_experiment_group(self):
        object = ExperimentGroupConfig(faker.word(),
                                       uuid=uuid.uuid4().hex,
                                       project=uuid.uuid4().hex)
        experiment_group_uuid = object.uuid
        httpretty.register_uri(
            httpretty.PATCH,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                experiment_group_uuid),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment_group(experiment_group_uuid, {'content': 'new'})
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_delete_experiment_group(self):
        experiment_group_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.DELETE,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                experiment_group_uuid),
            content_type='application/json',
            status=204)
        result = self.client.delete_experiment_group(experiment_group_uuid)
        assert result.status_code == 204
