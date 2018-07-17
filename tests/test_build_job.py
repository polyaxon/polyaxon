# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.build_job import BuildJobClient
from polyaxon_schemas.job import JobConfig, JobStatusConfig

faker = Faker()


class TestBuildJobClient(TestCase):
    def setUp(self):
        self.client = BuildJobClient(host='localhost',
                                     http_port=8000,
                                     ws_port=1337,
                                     version='v1',
                                     token=faker.uuid4(),
                                     reraise=True)

    @httpretty.activate
    def test_get_build(self):
        job = JobConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1
            ),
            body=json.dumps(job),
            content_type='application/json',
            status=200)
        result = self.client.get_build('username', 'project_name', 1)
        assert job == result.to_dict()

    @httpretty.activate
    def test_update_build(self):
        job = JobConfig(config={})
        httpretty.register_uri(
            httpretty.PATCH,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_build('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_delete_build(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1),
            content_type='application/json',
            status=204)
        result = self.client.delete_build('username', 'project_name', 1)
        assert result.status_code == 204

    @httpretty.activate
    def test_get_job_statuses(self):
        job = JobStatusConfig(id=1,
                              uuid=uuid.uuid4().hex,
                              job=1,
                              created_at=datetime.datetime.now(),
                              status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1,
                'statuses'),
            body=json.dumps({'results': [job], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_stop_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_bookmark_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1,
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.client.bookmark('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_unbookmark_build(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.client.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_job_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            BuildJobClient._build_url(
                self.client.base_url,
                BuildJobClient.ENDPOINT,
                'username',
                'project_name',
                'builds',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.client.logs('username', 'project_name', 1, stream=False)
        assert response.content.decode() == 'some text'
