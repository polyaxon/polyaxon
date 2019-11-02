# coding: utf-8
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from mock import mock, MagicMock

from polyaxon import settings
from polyaxon.client.statuses import get_run_statuses


class TestStatuses(TestCase):

    @mock.patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_get_statuses(self, sdk_get_run_statuses):
        for _ in get_run_statuses(owner="owner", project="project", run_uuid=uuid.uuid4().hex):
            pass
        assert sdk_get_run_statuses.call_count == 1

    @mock.patch("polyaxon_sdk.RunsV1Api.get_run_statuses")
    def test_get_statuses_watch(self, sdk_get_run_statuses):
        settings.CLIENT_CONFIG.watch_interval = 1
        for _ in get_run_statuses(
            owner="owner",
            project="project",
            run_uuid=uuid.uuid4().hex,
            watch=True
        ):
            resp = MagicMock(status="failed", status_conditions=[])
            sdk_get_run_statuses.return_value = resp
        assert sdk_get_run_statuses.call_count == 2
