# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from collections import Mapping

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.build_job import BuildJobApi
from polyaxon_client.schemas import BuildJobConfig, JobStatusConfig
from polyaxon_schemas.api.code_reference import CodeReferenceConfig


class TestBuildJobApi(TestBaseApi):

    def setUp(self):
        super(TestBuildJobApi, self).setUp()
        self.api_handler = BuildJobApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_build(self):
        job = BuildJobConfig().to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1
            ),
            body=json.dumps(job),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.get_build('username', 'project_name', 1)
        assert result.to_dict() == job

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_build('username', 'project_name', 1)
        assert result == job

    @httpretty.activate
    def test_update_build(self):
        job = BuildJobConfig().to_dict()
        httpretty.register_uri(
            httpretty.PATCH,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1),
            body=json.dumps(job),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.update_build('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == job

        # Raw response
        self.set_raw_response()
        result = self.api_handler.update_build('username', 'project_name', 1, {'name': 'new'})
        assert result == job

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.update_build(
                'username', 'project_name', 1, {'name': 'new'}, background=True),
            method='patch')

    @httpretty.activate
    def test_delete_build(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1),
            content_type='application/json',
            status=204)
        result = self.api_handler.delete_build('username', 'project_name', 1)
        assert result.status_code == 204

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.delete_build(
                'username', 'project_name', 1, background=True),
            method='delete')

    @httpretty.activate
    def test_get_job_statuses(self):
        job = JobStatusConfig(id=1,
                              uuid=uuid.uuid4().hex,
                              job=1,
                              created_at=datetime.datetime.now(),
                              status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'statuses'),
            body=json.dumps({'results': [job], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], JobStatusConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_create_build_status(self):
        exp = JobStatusConfig(id=1,
                              uuid=uuid.uuid4().hex,
                              job=1,
                              created_at=datetime.datetime.now(),
                              status='Running').to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'statuses'),
            body=json.dumps(exp),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.create_status('username',
                                                  'project_name',
                                                  1,
                                                  status='running')
        assert response.to_dict() == exp

        # Raw response
        self.set_raw_response()
        response = self.api_handler.create_status('username',
                                                  'project_name',
                                                  1,
                                                  traceback='traceback',
                                                  status='failed')
        assert response == exp

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.create_status(
                'username',
                'project_name',
                1,
                traceback='traceback',
                status='running',
                background=True),
            method='post')

    @httpretty.activate
    def test_create_build_code_reference(self):
        coderef = CodeReferenceConfig(commit='3783ab36703b14b91b15736fe4302bfb8d52af1c',
                                      head='3783ab36703b14b91b15736fe4302bfb8d52af1c',
                                      branch='feature1',
                                      git_url='https://bitbucket.org:foo/bar.git',
                                      is_dirty=True).to_dict()
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'coderef'),
            body=json.dumps(coderef),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.create_code_reference(
            'username', 'project_name', 1, coderef=coderef)
        assert response.to_dict() == coderef

        # Raw response
        self.set_raw_response()
        response = self.api_handler.create_code_reference(
            'username', 'project_name', 1, coderef=coderef)
        assert response == coderef

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.create_code_reference(
                'username', 'project_name', 1, coderef=coderef, background=True),
            method='post')

    @httpretty.activate
    def test_stop_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.stop(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_invalidate_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'invalidate'),
            content_type='application/json',
            status=200)
        result = self.api_handler.invalidate('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.invalidate(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_bookmark_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.bookmark('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.bookmark(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_unbookmark_build(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.unbookmark(
                'username', 'project_name', 1, background=True),
            method='delete')

    @httpretty.activate
    def test_create_build_logs(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'logs'),
            body=json.dumps({'log_lines': 'foo\nbar'}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.send_logs('username', 'project_name', 1, log_lines='foo\nbar')
        assert response.status_code == 200

        # Raw response
        self.set_raw_response()
        response = self.api_handler.send_logs('username', 'project_name', 1, log_lines='foo\nbar')
        assert response.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.send_logs(
                'username', 'project_name', 1,
                log_lines='foo\nbar',
                background=True),
            method='post')

        # Periodic
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.send_logs(
                'username', 'project_name', 1,
                log_lines='foo\nbar',
                periodic=True),
            method='post')

    @httpretty.activate
    def test_job_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.api_handler.logs('username', 'project_name', 1, stream=False)
        assert response.content.decode() == 'some text'

    def test_get_heartbeat_url(self):
        self.assertEqual(self.api_handler.get_heartbeat_url('username', 'project_name', 1),
                         BaseApiHandler.build_url(
                             self.api_config.base_url,
                             '/',
                             'username',
                             'project_name',
                             'builds',
                             1,
                             BaseApiHandler.HEARTBEAT))
