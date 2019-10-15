# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import uuid

from collections import Mapping

from tests.test_client_api.utils import TestBaseApi

from polyaxon.client.api.base import BaseApiHandler
from polyaxon.client.api.bookmark import BookmarkApi
from polyaxon.schemas.api.experiment import ExperimentConfig
from polyaxon.schemas.api.project import ProjectConfig


class TestBookmarkApi(TestBaseApi):
    def setUp(self):
        super(TestBookmarkApi, self).setUp()
        self.api_handler = BookmarkApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_bookmarked_experiments(self):
        project_uuid = uuid.uuid4().hex
        obj_uuid = uuid.uuid4().hex
        objs = [
            {
                "content_object": ExperimentConfig(
                    uuid=obj_uuid, project=project_uuid
                ).to_dict()
            }
            for _ in range(10)
        ]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url, "/bookmarks", "user", "experiments"
            ),
            body=json.dumps({"results": objs, "count": 10, "next": None}),
            content_type="application/json",
            status=200,
        )

        # Schema response
        result = self.api_handler.experiments("user")
        assert len(result["results"]) == 10
        assert isinstance(result["results"][0], ExperimentConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.experiments("user")
        assert len(result["results"]) == 10
        assert isinstance(result["results"][0], Mapping)

    @httpretty.activate
    def test_get_bookmarked_projects(self):
        projects = [
            {"content_object": ProjectConfig("proj").to_dict()} for _ in range(10)
        ]
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url, "/bookmarks", "user", "projects"
            ),
            body=json.dumps({"results": projects, "count": 10, "next": None}),
            content_type="application/json",
            status=200,
        )

        # Schema response
        result = self.api_handler.projects("user")
        assert len(result["results"]) == 10
        assert isinstance(result["results"][0], ProjectConfig)

        # Raw response
        self.set_raw_response()
        result = self.api_handler.projects("user")
        assert len(result["results"]) == 10
        assert isinstance(result["results"][0], Mapping)
