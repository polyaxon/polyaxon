# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid
from unittest import TestCase
import httpretty
from faker import Faker
from polyaxon_schemas.experiment import ExperimentConfig

from polyaxon_schemas.project import ProjectConfig, ExperimentGroupConfig

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
            content_type='application/json',
            status=200)

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
            content_type='application/json',
            status=200)
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
            content_type='application/json',
            status=200)
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
            content_type='application/json',
            status=200)
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
            content_type='application/json',
            status=204)
        result = self.client.delete_project(project_uuid)
        assert result.status_code == 204

    @httpretty.activate
    def test_upload_repo(self):
        project_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.PUT,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'repo',
                'upload'),
            content_type='application/json',
            status=204)
        files = [('code', ('repo',
                           open('./tests/fixtures_static/repo.tar.gz', 'rb'),
                           'text/plain'))]
        result = self.client.upload_repo(project_uuid, files=files, files_size=10)
        assert result.status_code == 204

    @httpretty.activate
    def test_list_experiment_groups(self):
        project_uuid = uuid.uuid4().hex
        experiment_groups = [
            ExperimentGroupConfig(content=faker.word, project=project_uuid).to_dict()
            for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'experiment_groups'),
            body=json.dumps({'results': experiment_groups, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        experiment_groups = self.client.list_experiment_groups(project_uuid)
        assert len(experiment_groups) == 10

    @httpretty.activate
    def test_create_experiment_group(self):
        project_uuid = uuid.uuid4().hex
        object = ExperimentGroupConfig(content=faker.word(), project=project_uuid)
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'experiment_groups'),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment_group(project_uuid, object)
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_update_experiment_group(self):
        object = ExperimentGroupConfig(faker.word(),
                                       uuid=uuid.uuid4().hex,
                                       project=uuid.uuid4().hex)
        experiment_group_uuid = object.uuid
        project_uuid = object.project
        httpretty.register_uri(
            httpretty.PATCH,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'experiment_groups',
                experiment_group_uuid),
            body=json.dumps(object.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_experiment_group(project_uuid,
                                                     experiment_group_uuid,
                                                     {'content': 'new'})
        assert result.to_dict() == object.to_dict()

    @httpretty.activate
    def test_delete_experiment_group(self):
        project_uuid = uuid.uuid4().hex
        experiment_group_uuid = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.DELETE,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'experiment_groups',
                experiment_group_uuid),
            content_type='application/json',
            status=204)
        result = self.client.delete_experiment_group(project_uuid, experiment_group_uuid)
        assert result.status_code == 204

    @httpretty.activate
    def test_list_experiments(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(name='xp', uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'experiments'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_experiments(project_uuid)
        assert len(xps_results) == 10

        # pagination

        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.base_url,
                ProjectClient.ENDPOINT,
                project_uuid,
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        xps_results = self.client.list_experiments(project_uuid, page=2)
        assert len(xps_results) == 10
