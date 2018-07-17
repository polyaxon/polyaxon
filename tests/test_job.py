# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from faker import Faker
from unittest import TestCase

from polyaxon_client.job import JobClient
from polyaxon_schemas.job import JobConfig, JobStatusConfig

faker = Faker()


class TestJobClient(TestCase):
    def setUp(self):
        self.client = JobClient(host='localhost',
                                http_port=8000,
                                ws_port=1337,
                                version='v1',
                                token=faker.uuid4(),
                                reraise=True)

    @httpretty.activate
    def test_get_job(self):
        job = JobConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1
            ),
            body=json.dumps(job),
            content_type='application/json',
            status=200)
        result = self.client.get_job('username', 'project_name', 1)
        assert job == result.to_dict()

    @httpretty.activate
    def test_update_job(self):
        job = JobConfig(config={})
        httpretty.register_uri(
            httpretty.PATCH,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.update_job('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_delete_job(self):
        httpretty.register_uri(
            httpretty.DELETE,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1),
            content_type='application/json',
            status=204)
        result = self.client.delete_job('username', 'project_name', 1)
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
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'statuses'),
            body=json.dumps({'results': [job], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)
        response = self.client.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1

    @httpretty.activate
    def test_restart_job(self):
        job = JobConfig(config={})
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'restart'),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.restart('username', 'project_name', 1)
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_resume_job_with_config_and_latest_code(self):
        job = JobConfig(config={})
        config = {'config': {'logging': {'level': 'error'}}}
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'resume'),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.resume('username', 'project_name', 1, config, update_code=True)
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_resume_job(self):
        job = JobConfig(config={})
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'resume'),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.resume('username', 'project_name', 1)
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_resume_job_with_config(self):
        job = JobConfig(config={})
        config = {'config': {'logging': {'level': 'error'}}}
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'resume'),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.resume('username', 'project_name', 1, config)
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_copy_job(self):
        job = JobConfig(config={})
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'copy'),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.copy('username', 'project_name', 1)
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_copy_job_with_config(self):
        job = JobConfig(config={})
        config = {'config': {'declarations': {'lr': 0.1}}}
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'copy'),
            body=json.dumps(job.to_dict()),
            content_type='application/json',
            status=200)
        result = self.client.copy('username', 'project_name', 1, config)
        assert result.to_dict() == job.to_dict()

    @httpretty.activate
    def test_stop_job(self):
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.client.stop('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_job_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.client.logs('username', 'project_name', 1, stream=False)
        assert response.content.decode() == 'some text'

    @httpretty.activate
    def test_bookmark_job(self):
        httpretty.register_uri(
            httpretty.POST,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.client.bookmark('username', 'project_name', 1)
        assert result.status_code == 200

    @httpretty.activate
    def test_unbookmark_job(self):
        httpretty.register_uri(
            httpretty.DELETE,
            JobClient._build_url(
                self.client.base_url,
                JobClient.ENDPOINT,
                'username',
                'project_name',
                'jobs',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.client.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200
