# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from collections import Mapping

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.bookmark import BookmarkApi
from polyaxon_client.schemas import ExperimentConfig, GroupConfig, JobConfig, ProjectConfig


class TestBookmarkApi(TestBaseApi):

    def setUp(self):
        super(TestBookmarkApi, self).setUp()
        self.api_handler = BookmarkApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_bookmarked_builds(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [{'content_object': JobConfig(uuid=obj_uuid,
                                             project=project_uuid).to_dict()}
                for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/bookmarks',
                'user',
                'builds'),
            body=json.dumps({'results': objs, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.builds('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], JobConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.builds('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], Mapping)

    @httpretty.activate
    def test_get_bookmarked_jobs(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [{'content_object': JobConfig(uuid=obj_uuid,
                                             project=project_uuid).to_dict()}
                for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/bookmarks',
                'user',
                'jobs'),
            body=json.dumps({'results': objs, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.jobs('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], JobConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.jobs('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], Mapping)

    @httpretty.activate
    def test_get_bookmarked_experiments(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [{'content_object': ExperimentConfig(uuid=obj_uuid,
                                                    project=project_uuid).to_dict()}
                for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/bookmarks',
                'user',
                'experiments'),
            body=json.dumps({'results': objs, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.experiments('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], ExperimentConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.experiments('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], Mapping)

    @httpretty.activate
    def test_get_bookmarked_groups(self):
        project_uuid = uuid.uuid4().hex
        experiment_groups = [
            {'content_object': GroupConfig(content='text', project=project_uuid).to_dict()}
            for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/bookmarks',
                'user',
                'groups'),
            body=json.dumps({'results': experiment_groups, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.groups('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], GroupConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.groups('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], Mapping)

    @httpretty.activate
    def test_get_bookmarked_projects(self):
        projects = [{'content_object': ProjectConfig('proj').to_dict()} for _ in range(10)]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/bookmarks',
                'user',
                'projects'),
            body=json.dumps({'results': projects, 'count': 10, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.projects('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], ProjectConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.projects('user')
        assert len(result['results']) == 10
        assert isinstance(result['results'][0], Mapping)
