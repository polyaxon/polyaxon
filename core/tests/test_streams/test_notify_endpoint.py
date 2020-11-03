#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from asyncio import Future
from mock import patch

from polyaxon_sdk import V1StatusCondition

from polyaxon import settings
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import V1K8sResourceSchema
from polyaxon.lifecycle import V1Statuses
from polyaxon.schemas.types import V1ConnectionType
from polyaxon.streams.app.main import STREAMS_URL
from tests.test_streams.base import get_streams_client, set_store
from tests.utils import BaseTestCase


class TestNotifyEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.store_root = set_store()
        settings.AGENT_CONFIG.notification_connections = [
            V1ConnectionType(
                name="slack",
                kind=V1ConnectionKind.SLACK,
                secret=V1K8sResourceSchema(name="some"),
            )
        ]

        self.client = get_streams_client()
        self.base_url = STREAMS_URL + "/namespace/owner/project/runs/uuid/notify"

    def test_notify_with_no_data(self):
        response = self.client.post(self.base_url, json={})
        assert response.status_code == 400

    def test_notify_with_no_condition(self):
        data = {"name": "test", "condition": None, "connections": ["test"]}
        response = self.client.post(self.base_url, json=data)
        assert response.status_code == 400

    def test_notify_with_no_notifications(self):
        data = {
            "name": "test",
            "condition": V1StatusCondition(
                type=V1Statuses.FAILED, status=True
            ).to_dict(),
            "connections": None,
        }
        response = self.client.post(self.base_url, json=data)
        assert response.status_code == 400

        data = {
            "name": "test",
            "condition": V1StatusCondition(
                type=V1Statuses.FAILED, status=True
            ).to_dict(),
            "connections": [],
        }
        response = self.client.post(self.base_url, json=data)
        assert response.status_code == 400

    def test_notify_with_no_agent_notification_connections(self):
        settings.AGENT_CONFIG.notification_connections = []
        data = {
            "name": "test",
            "condition": V1StatusCondition(
                type=V1Statuses.FAILED, status=True
            ).to_dict(),
            "connections": ["test1", "test2"],
        }
        response = self.client.post(self.base_url, json=data)
        assert response.status_code == 400

    def test_notify_with_non_recognized_connections(self):
        data = {
            "name": "test",
            "condition": V1StatusCondition(
                type=V1Statuses.FAILED, status=True
            ).to_dict(),
            "connections": ["test1", "test2"],
        }
        with patch(
            "polyaxon.agents.spawners.async_spawner.AsyncK8SManager"
        ) as manager_mock:
            manager_mock.return_value.setup.return_value = Future()
            manager_mock.return_value.setup.return_value.set_result(None)
            response = self.client.post(self.base_url, json=data)
            assert response.status_code == 200
