# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.bookmark import BookmarkClient
from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.job import JobConfig
from polyaxon_schemas.project import ExperimentGroupConfig, ProjectConfig

faker = Faker()


class TestBookmarkClient(TestCase):
    def setUp(self):
        self.client = BookmarkClient(host='localhost',
                                     http_port=8000,
                                     ws_port=1337,
                                     version='v1',
                                     token=faker.uuid4(),
                                     reraise=True)

    @httpretty.activate
    def test_get_bookmarked_builds(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [{'content_object': JobConfig(config={},
                                             uuid=obj_uuid,
                                             project=project_uuid).to_dict()}
                for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BookmarkClient._build_url(
                self.client.base_url,
                BookmarkClient.ENDPOINT,
                'user',
                'builds'),
            body=json.dumps({'results': objs, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)
        result = self.client.builds('user')
        assert len(result['results']) == 10

    @httpretty.activate
    def test_get_bookmarked_jobs(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [{'content_object': JobConfig(config={},
                                             uuid=obj_uuid,
                                             project=project_uuid).to_dict()}
                for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BookmarkClient._build_url(
                self.client.base_url,
                BookmarkClient.ENDPOINT,
                'user',
                'jobs'),
            body=json.dumps({'results': objs, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)
        result = self.client.jobs('user')
        assert len(result['results']) == 10

    @httpretty.activate
    def test_get_bookmarked_experiments(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [{'content_object': ExperimentConfig(config={},
                                                    uuid=obj_uuid,
                                                    project=project_uuid).to_dict()}
                for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BookmarkClient._build_url(
                self.client.base_url,
                BookmarkClient.ENDPOINT,
                'user',
                'experiments'),
            body=json.dumps({'results': objs, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)
        result = self.client.experiments('user')
        assert len(result['results']) == 10

    @httpretty.activate
    def test_get_bookmarked_groups(self):
        project_uuid = uuid.uuid4().hex
        experiment_groups = [
            {'content_object': ExperimentGroupConfig(content=faker.word,
                                                     project=project_uuid).to_dict()}
            for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BookmarkClient._build_url(
                self.client.base_url,
                BookmarkClient.ENDPOINT,
                'user',
                'groups'),
            body=json.dumps({'results': experiment_groups, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)
        result = self.client.groups('user')
        assert len(result['results']) == 10

    @httpretty.activate
    def test_get_bookmarked_projects(self):
        projects = [{'content_object': ProjectConfig(faker.word).to_dict()} for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BookmarkClient._build_url(
                self.client.base_url,
                BookmarkClient.ENDPOINT,
                'user',
                'projects'),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)
        result = self.client.projects('user')
        assert len(result['results']) == 10
