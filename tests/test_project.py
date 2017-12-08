# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker

from polyaxon_schemas.project import ProjectConfig

from polyaxon_client.project import ProjectClient

faker = Faker()


class TestProjectClient(TestCase):

    def setUp(self):
        self.client = ProjectClient(host='http://localhost', version='v1')
        self.base_url = ProjectClient.BASE_URL.format('http://localhost', 'v1')

    @httpretty.activate
    def test_get_projects(self):
        projects = [ProjectConfig(faker.word).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json', status=200)

        projects = self.client.list_projects()
        assert len(projects) == 10

    @httpretty.activate
    def test_get_by_name(self):
        object = ProjectConfig(faker.word()).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                'uuid'),
            body=json.dumps(object),
            content_type='application/json', status=200)
        result = self.client.get_project('uuid')
        assert object == result.to_dict()

    @httpretty.activate
    def test_create_project(self):
        object = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT),
            body=json.dumps(object.to_dict()),
            content_type='application/json', status=200)
        result = self.client.create_project(object)
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_update_project(self):
        object = ProjectConfig(faker.word())
        project_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.PATCH,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid),
            body=json.dumps(object.to_dict()),
            content_type='application/json', status=200)
        result = self.client.update_project(project_uuid, {'name': 'new'})
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_delete_project(self):
        project_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.DELETE,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid),
            content_type='application/json', status=204)
        result = self.client.delete_project(project_uuid)
        assert result is None
