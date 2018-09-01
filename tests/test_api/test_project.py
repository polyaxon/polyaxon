# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import uuid

import httpretty
from faker import Faker

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.project import ProjectApi
from polyaxon_client.schemas import (
    ExperimentConfig,
    ExperimentGroupConfig,
    JobConfig,
    ProjectConfig,
    TensorboardJobConfig
)
from tests.test_api.utils import TestBaseApi

faker = Faker()


class TestProjectApi(TestBaseApi):

    def setUp(self):
        super(TestProjectApi, self).setUp()
        self.api_handler = ProjectApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_list_projects(self):
        projects = [ProjectConfig(faker.word).to_dict() for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user'
            ),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_projects('user')
        assert len(response['results']) == 10
        assert response['count'] == 10
        assert response['next'] is None
        assert response['previous'] is None

    @httpretty.activate
    def test_get_project(self):
        obj = ProjectConfig(faker.word()).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.api_handler.get_project('user', 'project')
        assert obj == result.to_dict()

    @httpretty.activate
    def test_create_project(self):
        obj = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                'projects'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_project(obj)
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_update_project(self):
        obj = ProjectConfig(faker.word())
        httpretty.register_uri(
            httpretty.PATCH,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.update_project('user', 'project', {'name': 'new'})
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_delete_project(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project'),
            content_type='application/json',
            status=204)
        result = self.api_handler.delete_project('user', 'project')
        assert result.status_code == 204

    @httpretty.activate
    def test_upload_repo(self):
        httpretty.register_uri(
            httpretty.PUT,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'repo',
                'upload'),
            content_type='application/json',
            status=204)
        files = [('code', ('repo',
                           open('./tests/fixtures_static/repo.tar.gz', 'rb'),
                           'text/plain'))]
        result = self.api_handler.upload_repo('user', 'project', files=files, files_size=10)
        assert result.status_code == 204

    @httpretty.activate
    def test_upload_repo_synchronous(self):
        httpretty.register_uri(
            httpretty.PUT,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'repo',
                'upload'),
            content_type='application/json',
            status=204)
        files = [('code', ('repo',
                           open('./tests/fixtures_static/repo.tar.gz', 'rb'),
                           'text/plain'))]
        result = self.api_handler.upload_repo('user',
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'groups'),
            body=json.dumps({'results': experiment_groups, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_experiment_groups('user', 'project')
        assert len(response['results']) == 10

    @httpretty.activate
    def test_create_experiment_group(self):
        project_uuid = uuid.uuid4().hex
        obj = ExperimentGroupConfig(content=faker.word(), project=project_uuid)
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'groups'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_experiment_group('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create with dict
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'groups'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_experiment_group('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_list_experiments(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [ExperimentConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_experiments('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_experiments('user', 'project', page=2)
        assert len(response['results']) == 10

        # metrics & declarations
        for xp in xps:
            xp['metrics'] = {'loss': 0.1}
            xp['declarations'] = {'foo': 'bar'}

        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments') + '?metrics=true',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_experiments('user', 'project', metrics=True, page=2)

        assert len(response['results']) == 10
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments') + '?declarations=true',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_experiments('user', 'project', declarations=True, page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'experiments') + '?independent=true&query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_experiments('user',
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_experiment('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create experiment with dict
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_experiment('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_list_jobs(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [JobConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'jobs'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_jobs('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'jobs') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_jobs('user', 'project', page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'jobs') + '?query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_jobs('user',
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'jobs'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_job('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create experiment with dict
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'jobs'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_job('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_list_tensorboards(self):
        project_uuid = uuid.uuid4().hex
        xp_uuid = uuid.uuid4().hex
        xps = [TensorboardJobConfig(config={}, uuid=xp_uuid, project=project_uuid).to_dict()
               for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'tensorboards'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_tensorboards('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'tensorboards') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_tensorboards('user', 'project', page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'tensorboards') + '?query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_tensorboards('user',
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'builds'),
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_builds('user', 'project')
        assert len(response['results']) == 10

        # pagination
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'builds') + '?offset=2',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_builds('user', 'project', page=2)
        assert len(response['results']) == 10

        # query, sort
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds') + '?query=started_at:>=2010-10-10,sort=created_at',
            body=json.dumps({'results': xps, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        response = self.api_handler.list_builds('user',
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
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'builds'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_build('user', 'project', obj)
        assert result.to_dict() == obj.to_dict()

        # Test create experiment with dict
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'builds'),
            body=json.dumps(obj.to_dict()),
            content_type='application/json',
            status=200)
        result = self.api_handler.create_build('user', 'project', obj.to_dict())
        assert result.to_dict() == obj.to_dict()

    @httpretty.activate
    def test_start_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'tensorboard',
                'start'),
            content_type='application/json',
            status=200)
        result = self.api_handler.start_tensorboard('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_start_tensorboard_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'tensorboard',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.api_handler.start_tensorboard('username', 'project_name', obj)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_tensorboard(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'tensorboard',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop_tensorboard('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_start_notebook(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'notebook',
                'start'),
            content_type='application/json',
            status=200)
        result = self.api_handler.start_notebook('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_start_notebook_with_config(self):
        obj = {}
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'notebook',
                'start'),
            body=json.dumps(obj),
            content_type='application/json',
            status=200)
        result = self.api_handler.start_notebook('username', 'project_name', obj)
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_notebook(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'notebook',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop_notebook('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_stop_notebook_without_commit(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'notebook',
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop_notebook('username', 'project_name', commit=False)
        assert result.status_code == 200

    @httpretty.activate
    def test_bookmark_project(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.bookmark('username', 'project_name')
        assert result.status_code == 200

    @httpretty.activate
    def test_unbookmark_project(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler._build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.unbookmark('username', 'project_name')
        assert result.status_code == 200
