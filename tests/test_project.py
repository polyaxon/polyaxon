# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.project import ProjectClient
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.job import JobConfig, TensorboardJobConfig
from polyaxon_schemas.project import ExperimentGroupConfig, ProjectConfig

faker = Faker()


class TestProjectClient(TestCase):
    def setUp(self):
        self.client = ProjectClient(host='localhost',
                                    http_port=8000,
                                    ws_port=1337,
                                    version='v1',
                                    token=faker.uuid4(),
                                    reraise=True)

    @httpretty.activate
    def test_list_projects(self):
        projects = [ProjectConfig(faker.word).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user'
            ),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_projects('user')
        assert len(response['results']) == 10
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

    @httpretty.activate
    def test_get_project(self):
        obj = ProjectConfig(faker.word()).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.get_project('user', 'project')
        assert obj == result.to_dict()

    @httpretty.activate
    def test_create_project(self):
        obj = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                'projects'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_project(obj)
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_update_project(self):
        obj = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.PATCH,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_project('user', 'project', {'name': 'new'})
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_delete_project(self):
        httpretty.register_uri(
            httpretty.DELETE,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project'),
            content_type='application/json',
            status=204)
        result = self.client.delete_project('user', 'project')
        assert result.status_code == 204

    @httpretty.activate
    def test_upload_repo(self):
        httpretty.register_uri(
            httpretty.PUT,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'repo',
                'upload'),
            content_type='application/json',
            status=204)
        files = [('code', ('repo',
                           open('./tests/fixtures_static/repo.tar.gz', 'rb'),
                           'text/plain'))]
        result = self.client.upload_repo('user', 'project', files=files, files_size=10)
        assert result.status_code == 204

    @httpretty.activate
    def test_upload_repo_synchronous(self):
        httpretty.register_uri(
            httpretty.PUT,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'repo',
                'upload'),
            content_type='application/json',
            status=204)
        files = [('code', ('repo',
                           open('./tests/fixtures_static/repo.tar.gz', 'rb'),
                           'text/plain'))]
        result = self.client.upload_repo('user',
                                         'project',
                                         files=files,
                                         files_size=10,
                                         upload_async=False)
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
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'groups'),
            body=json.dumps({'results': experiment_groups, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiment_groups('user', 'project')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_experiment_group(self):
        project_uuid = uuid.uuid4().hex
        obj = ExperimentGroupConfig(content=faker.word(), project=project_uuid)
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'groups'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment_group('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create with dict
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'groups'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment_group('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_list_experiments(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user', 'project', page=2)
        assert len(response['results']) == 10

        # metrics & declarations
        for xp in xps:
            xp['metrics'] = {'loss': 0.1}
            xp['declarations'] = {'foo': 'bar'}

        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments') + '?metrics=true',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user', 'project', metrics=True, page=2)

        assert len(response['results']) == 10
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments') + '?declarations=true',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user', 'project', declarations=True, page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'experiments') + '?independent=true&query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_experiments('user',
                                                'project',
                                                True,
                                                query='started_at:>=2010-10-10',
                                                sort='created_at')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_experiment(self):
        project_uuid = uuid.uuid4().hex
        obj = ExperimentConfig(project=project_uuid, config={})
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create experiment with dict
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'experiments'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_experiment('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_list_jobs(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [JobConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'jobs'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_jobs('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'jobs') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_jobs('user', 'project', page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'jobs') + '?query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_jobs('user',
                                         'project',
                                         query='started_at:>=2010-10-10',
                                         sort='created_at')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_job(self):
        project_uuid = uuid.uuid4().hex
        obj = JobConfig(project=project_uuid, config={})
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'jobs'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_job('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create experiment with dict
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'jobs'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_job('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_list_tensorboards(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [TensorboardJobConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'tensorboards'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_tensorboards('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'tensorboards') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_tensorboards('user', 'project', page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'tensorboards') + '?query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_tensorboards('user',
                                                 'project',
                                                 query='started_at:>=2010-10-10',
                                                 sort='created_at')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_list_builds(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [JobConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'builds'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_builds('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'builds') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_builds('user', 'project', page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'builds') + '?query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.client.list_builds('user',
                                           'project',
                                           query='started_at:>=2010-10-10',
                                           sort='created_at')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_build(self):
        project_uuid = uuid.uuid4().hex
        obj = JobConfig(project=project_uuid, config={})
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'builds'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_build('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create experiment with dict
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'user',
                'project',
                'builds'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.create_build('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_start_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'tensorboard',
                'start'),
            content_type='application/json',
            status=200)
        result = self.client.start_tensorboard('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_start_tensorboard_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'tensorboard',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.start_tensorboard('username', 'project_name', obj)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'tensorboard',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop_tensorboard('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_start_notebook(self):
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'notebook',
                'start'),
            content_type='application/json',
            status=200)
        result = self.client.start_notebook('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_start_notebook_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'notebook',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.client.start_notebook('username', 'project_name', obj)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_notebook(self):
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'notebook',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop_notebook('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_notebook_without_commit(self):
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'notebook',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop_notebook('username', 'project_name', commit=False)
        assert result.status_code == 200

    @httpretty.activate
    def test_bookmark_project(self):
        httpretty.register_uri(
            httpretty.POST,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.client.bookmark('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_unbookmark_project(self):
        httpretty.register_uri(
            httpretty.DELETE,
            ProjectClient._build_url(
                self.client.base_url,
                ProjectClient.ENDPOINT,
                'username',
                'project_name',
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.client.unbookmark('username', 'project_name')
        assert result.status_code == 200
