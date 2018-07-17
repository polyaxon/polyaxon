# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.experiment_group import ExperimentGroupClient
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig, GroupStatusConfig

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
    def test_get_experiment_group(self):
        obj = ExperimentGroupConfig(content=faker.word(),
                                    uuid=uuid.uuid4().hex,
                                    project=uuid.uuid4().hex).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.get_experiment_group('username', 'project_name', 1)
        assert obj == result.to_dict()

    @httpretty.activate
    def test_list_experiments(self):
        group_uuid = uuid.uuid4().hex
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(uuid=xp_uuid,
                                config={},
                                project=project_uuid,
                                experiment_group=group_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'experiments') + '?group=1',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('username', 'project_name', 1)
        assert len(response['results']) == 10
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'experiments') + '?group=1&offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('username', 'project_name', 1, page=2)
        assert len(response['results']) == 10

        # query, sort

        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'experiments') + '?group=1&query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('username',
                                                'project_name',
                                                1,
                                                query='started_at:>=2010-10-10',
                                                sort='created_at')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_update_experiment_group(self):
        obj = ExperimentGroupConfig(content=faker.word(),
                                    uuid=uuid.uuid4().hex,
                                    project=uuid.uuid4().hex)
        httpretty.register_uri(
            httpretty.PATCH,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment_group(
            'username', 'project_name', 1, {'content': 'new'})
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_delete_experiment_group(self):
        httpretty.register_uri(
            httpretty.DELETE,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1),
            content_type='application/json',
            status=204)
        result = self.client.delete_experiment_group('username', 'project_name', 1)
        assert result.status_code == 204

    @httpretty.activate
    def test_get_experiment_group_statuses(self):
        group = GroupStatusConfig(id=1,
                                  uuid=uuid.uuid4().hex,
                                  experiment_group=1,
                                  created_at=datetime.datetime.now(),
                                  status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'statuses'),
            body=json.dumps({'results': [group], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_stop_experiment_group_all(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_experiment_group_pending(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop('username', 'project_name', 1, pending=True)
        assert result.status_code == 200

    @httpretty.activate
    def test_start_experiment_group_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'tensorboard',
                'start'),
            content_type='application/json',
            status=200)
        result = self.client.start_tensorboard('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_start_experiment_group_tensorboard_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'tensorboard',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.start_tensorboard('username', 'project_name', 1, obj)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_experiment_group_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
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
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
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
            ExperimentGroupClient._build_url(
                self.client.base_url,
                ExperimentGroupClient.ENDPOINT,
                'username',
                'project_name',
                'groups',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.client.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200
