# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.project import ProjectConfig

from polyaxon_client.project import ProjectClient

faker = Faker()


class TestProjectClient(TestCase):

    def setUp(self):
        self.client = ProjectClient(host='http://localhost', version='v1')

    @httpretty.activate
    def test_get_projects(self):
        projects = [ProjectConfig(faker.word).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                ProjectClient.BASE_URL.format('http://localhost', 'v1'),
                ProjectClient.ENDPOINT),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json', status=200)

        projects = self.client.get_projects()
        assert len(projects) == 10

    @httpretty.activate
    def test_get_by_name(self):
        object = ProjectConfig(faker.word).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                ProjectClient.BASE_URL.format('http://localhost', 'v1'),
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_by_name('user', 'project')
        assert object == result.to_dict()
