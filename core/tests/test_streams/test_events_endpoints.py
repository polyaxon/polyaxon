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
import os
import pandas as pd
import shutil

from tests.test_streams.base import get_streams_client, set_store
from tests.utils import BaseTestCase

from polyaxon import settings
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import V1Event, V1Events
from polyaxon.polyboard.events.schemas import LoggedEventListSpec
from polyaxon.streams.app.main import STREAMS_URL
from polyaxon.utils.path_utils import create_path


class TestEventsEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.store_root = set_store()
        self.run_path = os.path.join(self.store_root, "uuid")
        self.run_events = os.path.join(self.run_path, "events")
        # Create run artifacts path
        create_path(self.run_path)
        # Create run artifacts events path
        create_path(self.run_events)
        # Create run events
        self.create_tmp_events()

        self.client = get_streams_client()
        self.base_url = STREAMS_URL + "/namespace/owner/project/runs/uuid/events"

    def create_tmp_events(self):
        text1 = LoggedEventListSpec(
            name="text1",
            kind=V1ArtifactKind.TEXT,
            events=[
                V1Event.make(step=1, text="foo1"),
                V1Event.make(step=2, text="boo2"),
            ],
        )
        self.create_kind_events(name="text1", kind=V1ArtifactKind.TEXT, events=text1)
        text2 = LoggedEventListSpec(
            name="text2",
            kind=V1ArtifactKind.TEXT,
            events=[
                V1Event.make(step=1, text="foo2"),
                V1Event.make(step=2, text="boo2"),
            ],
        )
        self.create_kind_events(name="text2", kind=V1ArtifactKind.TEXT, events=text2)
        html1 = LoggedEventListSpec(
            name="html1",
            kind=V1ArtifactKind.HTML,
            events=[
                V1Event.make(step=1, html="foo1"),
                V1Event.make(step=2, html="boo2"),
            ],
        )
        self.create_kind_events(name="html1", kind=V1ArtifactKind.HTML, events=html1)
        html2 = LoggedEventListSpec(
            name="htm2",
            kind=V1ArtifactKind.HTML,
            events=[
                V1Event.make(step=1, html="foo2"),
                V1Event.make(step=2, html="boo2"),
            ],
        )
        self.create_kind_events(name="html2", kind=V1ArtifactKind.HTML, events=html2)

    def create_kind_events(self, name, kind, events):
        event_kind_path = "{}/{}".format(self.run_events, kind)
        create_path(event_kind_path)
        with open("{}/{}.plx".format(event_kind_path, name), "+w") as f:
            f.write(events.get_csv_header())
            f.write(events.get_csv_events())

    def test_download_events_cached(self):
        filepath1 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text1.plx"
        )
        filepath2 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text2.plx"
        )
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False
        response = self.client.get(self.base_url + "/text?names=text1,text2&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True

        shutil.rmtree(self.run_events)
        response = self.client.get(self.base_url + "/text?names=text1,text2&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True

        shutil.rmtree(
            os.path.join(settings.CLIENT_CONFIG.archive_root, "uuid", "events")
        )
        response = self.client.get(self.base_url + "/text?names=text1,text2&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False

    def test_download_events_cached_force(self):
        filepath1 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text1.plx"
        )
        filepath2 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text2.plx"
        )
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False
        response = self.client.get(self.base_url + "/text?names=text1,text2&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True

        shutil.rmtree(self.run_events)
        response = self.client.get(
            self.base_url + "/text?names=text1,text2&orient=csv&force=true"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False

    def test_download_text_events_as_csv(self):
        filepath1 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text1.plx"
        )
        filepath2 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text2.plx"
        )
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False
        response = self.client.get(self.base_url + "/text?names=text1&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is False
        events1 = V1Events.read(name="text1", kind=V1ArtifactKind.TEXT, data=filepath1)
        for res in response.json()["data"]:
            assert isinstance(res["data"], str)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        assert results[0].name == events1.name
        assert results[0].kind == events1.kind
        assert pd.DataFrame.equals(results[0].df, events1.df)

        response = self.client.get(self.base_url + "/text?names=text1,text2&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        events2 = V1Events.read(name="text2", kind=V1ArtifactKind.TEXT, data=filepath2)
        for res in response.json()["data"]:
            assert isinstance(res["data"], str)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

        response = self.client.get(
            self.base_url + "/text?names=text1,text2,text3&orient=csv"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        for res in response.json()["data"]:
            assert isinstance(res["data"], str)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

    def test_download_html_events_as_csv(self):
        filepath1 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "html", "html1.plx"
        )
        filepath2 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "html", "html2.plx"
        )
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False
        response = self.client.get(self.base_url + "/html?names=html1&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is False
        events1 = V1Events.read(name="html1", kind=V1ArtifactKind.HTML, data=filepath1)
        for res in response.json()["data"]:
            assert isinstance(res["data"], str)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        assert results[0].name == events1.name
        assert results[0].kind == events1.kind
        assert pd.DataFrame.equals(results[0].df, events1.df)

        response = self.client.get(self.base_url + "/html?names=html1,html2&orient=csv")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        events2 = V1Events.read(name="html2", kind=V1ArtifactKind.HTML, data=filepath2)
        for res in response.json()["data"]:
            assert isinstance(res["data"], str)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

        response = self.client.get(
            self.base_url + "/html?names=text1,html1,html2&orient=csv"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        for res in response.json()["data"]:
            assert isinstance(res["data"], str)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

    def test_download_text_events_as_dict(self):
        filepath1 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text1.plx"
        )
        filepath2 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "text", "text2.plx"
        )
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False
        response = self.client.get(self.base_url + "/text?names=text1&orient=dict")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is False
        events1 = V1Events.read(
            name="text1", kind=V1ArtifactKind.TEXT, data=filepath1, parse_dates=False
        )
        for res in response.json()["data"]:
            assert isinstance(res["data"], dict)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        assert results[0].name == events1.name
        assert results[0].kind == events1.kind
        assert pd.DataFrame.equals(results[0].df, events1.df)

        response = self.client.get(
            self.base_url + "/text?names=text1,text2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        events2 = V1Events.read(
            name="text2", kind=V1ArtifactKind.TEXT, data=filepath2, parse_dates=False
        )
        for res in response.json()["data"]:
            assert isinstance(res["data"], dict)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

        response = self.client.get(
            self.base_url + "/text?names=text1,text2,text3&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        for res in response.json()["data"]:
            assert isinstance(res["data"], dict)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

    def test_download_html_events_as_dict(self):
        filepath1 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "html", "html1.plx"
        )
        filepath2 = os.path.join(
            settings.CLIENT_CONFIG.archive_root, "uuid", "events", "html", "html2.plx"
        )
        assert os.path.exists(filepath1) is False
        assert os.path.exists(filepath2) is False
        response = self.client.get(self.base_url + "/html?names=html1&orient=dict")
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is False
        events1 = V1Events.read(
            name="html1", kind=V1ArtifactKind.HTML, data=filepath1, parse_dates=False
        )
        for res in response.json()["data"]:
            assert isinstance(res["data"], dict)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        assert results[0].name == events1.name
        assert results[0].kind == events1.kind
        assert pd.DataFrame.equals(results[0].df, events1.df)

        response = self.client.get(
            self.base_url + "/html?names=html1,html2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        events2 = V1Events.read(
            name="html2", kind=V1ArtifactKind.HTML, data=filepath2, parse_dates=False
        )
        for res in response.json()["data"]:
            assert isinstance(res["data"], dict)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)

        response = self.client.get(
            self.base_url + "/html?names=text1,html1,html2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath1) is True
        assert os.path.exists(filepath2) is True
        for res in response.json()["data"]:
            assert isinstance(res["data"], dict)
        results = [V1Events.read(**i) for i in response.json()["data"]]
        expected = {events1.name: events1, events2.name: events2}
        for res in results:
            exp = expected[res.name]
            assert res.name == exp.name
            assert res.kind == exp.kind
            assert pd.DataFrame.equals(res.df, exp.df)


class TestMultiRunsEventsEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.store_root = set_store()
        self.run1_path = os.path.join(self.store_root, "uuid1")
        self.run1_events = os.path.join(self.run1_path, "events")
        self.run2_path = os.path.join(self.store_root, "uuid2")
        self.run2_events = os.path.join(self.run2_path, "events")
        # Create run artifacts path
        create_path(self.run1_path)
        create_path(self.run2_path)
        # Create run artifacts events path
        create_path(self.run1_events)
        create_path(self.run2_events)
        # Create run events
        self.create_tmp_events(run_events=self.run1_events)
        self.create_tmp_events(run_events=self.run2_events)

        self.client = get_streams_client()
        self.base_url = STREAMS_URL + "/namespace/owner/project/runs/multi/events"

    def create_tmp_events(self, run_events: str):
        metric1 = LoggedEventListSpec(
            name="metric1",
            kind=V1ArtifactKind.METRIC,
            events=[
                V1Event.make(step=1, metric=1.1),
                V1Event.make(step=2, metric=1.2),
            ],
        )
        self.create_kind_events(
            run_events=run_events,
            name="metric1",
            kind=V1ArtifactKind.METRIC,
            events=metric1,
        )
        metric2 = LoggedEventListSpec(
            name="metric2",
            kind=V1ArtifactKind.METRIC,
            events=[
                V1Event.make(step=1, metric=2.1),
                V1Event.make(step=2, metric=2.2),
            ],
        )
        self.create_kind_events(
            run_events=run_events,
            name="metric2",
            kind=V1ArtifactKind.METRIC,
            events=metric2,
        )

    def create_kind_events(self, run_events, name, kind, events):
        event_kind_path = "{}/{}".format(run_events, kind)
        create_path(event_kind_path)
        with open("{}/{}.plx".format(event_kind_path, name), "+w") as f:
            f.write(events.get_csv_header())
            f.write(events.get_csv_events())

    def test_download_multi_metric_events_cached(self):
        filepath11 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath12 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric2.plx",
        )
        filepath21 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath22 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric2.plx",
        )

        response = self.client.get(
            self.base_url + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True

        shutil.rmtree(self.run1_path)
        shutil.rmtree(self.run2_path)

        response = self.client.get(
            self.base_url + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True

        shutil.rmtree(os.path.join(settings.CLIENT_CONFIG.archive_root, "uuid1"))
        response = self.client.get(
            self.base_url + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is False
        assert os.path.exists(filepath12) is False
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True

    def test_download_multi_metric_events_cached_force(self):
        filepath11 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath12 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric2.plx",
        )
        filepath21 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath22 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric2.plx",
        )

        response = self.client.get(
            self.base_url + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True

        shutil.rmtree(self.run1_path)
        shutil.rmtree(self.run2_path)

        response = self.client.get(
            self.base_url
            + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=dict&force=true"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is False
        assert os.path.exists(filepath12) is False
        assert os.path.exists(filepath21) is False
        assert os.path.exists(filepath22) is False

    def test_download_multi_metric_events_as_dict(self):
        filepath11 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath12 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric2.plx",
        )
        filepath21 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath22 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric2.plx",
        )
        assert os.path.exists(filepath11) is False
        assert os.path.exists(filepath12) is False
        assert os.path.exists(filepath21) is False
        assert os.path.exists(filepath22) is False
        response = self.client.get(
            self.base_url + "/metric?names=metric1&runs=uuid1&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is False
        assert os.path.exists(filepath21) is False
        assert os.path.exists(filepath22) is False
        events11 = V1Events.read(
            name="metric1",
            kind=V1ArtifactKind.METRIC,
            data=filepath11,
            parse_dates=False,
        )
        results = response.json()["data"]
        assert list(results.keys()) == ["uuid1"]
        assert len(results["uuid1"]) == 1
        results = [V1Events.read(**i) for i in response.json()["data"]["uuid1"]]
        assert results[0].name == events11.name
        assert results[0].kind == events11.kind
        assert pd.DataFrame.equals(results[0].df, events11.df)

        response = self.client.get(
            self.base_url + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True
        events12 = V1Events.read(
            name="metric2",
            kind=V1ArtifactKind.METRIC,
            data=filepath12,
            parse_dates=False,
        )
        events21 = V1Events.read(
            name="metric1",
            kind=V1ArtifactKind.METRIC,
            data=filepath21,
            parse_dates=False,
        )
        events22 = V1Events.read(
            name="metric2",
            kind=V1ArtifactKind.METRIC,
            data=filepath22,
            parse_dates=False,
        )
        expected = {
            "uuid1": {events11.name: events11, events12.name: events12},
            "uuid2": {events21.name: events21, events22.name: events22},
        }
        response = response.json()["data"]
        results = {
            run_uuid: [V1Events.read(**i) for i in response[run_uuid]]
            for run_uuid in response
        }
        for run_uuid in results:
            for res in results[run_uuid]:
                exp = expected[run_uuid][res.name]
                assert res.name == exp.name
                assert res.kind == exp.kind
                assert pd.DataFrame.equals(res.df, exp.df)

        response = self.client.get(
            self.base_url
            + "/metric?names=metric12,text2,text3&runs=uuid1,uuid2,uuid3&orient=dict"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True
        expected = {
            "uuid1": {events11.name: events11, events12.name: events12},
            "uuid2": {events21.name: events21, events22.name: events22},
        }
        response = response.json()["data"]
        results = {
            run_uuid: [V1Events.read(**i) for i in response[run_uuid]]
            for run_uuid in response
        }
        for run_uuid in results:
            for res in results[run_uuid]:
                exp = expected[run_uuid][res.name]
                assert res.name == exp.name
                assert res.kind == exp.kind
                assert pd.DataFrame.equals(res.df, exp.df)

    def test_download_multi_metric_events_as_csv(self):
        filepath11 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath12 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid1",
            "events",
            "metric",
            "metric2.plx",
        )
        filepath21 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric1.plx",
        )
        filepath22 = os.path.join(
            settings.CLIENT_CONFIG.archive_root,
            "uuid2",
            "events",
            "metric",
            "metric2.plx",
        )
        assert os.path.exists(filepath11) is False
        assert os.path.exists(filepath12) is False
        assert os.path.exists(filepath21) is False
        assert os.path.exists(filepath22) is False
        response = self.client.get(
            self.base_url + "/metric?names=metric1&runs=uuid1&orient=csv"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is False
        assert os.path.exists(filepath21) is False
        assert os.path.exists(filepath22) is False
        events11 = V1Events.read(
            name="metric1", kind=V1ArtifactKind.METRIC, data=filepath11
        )
        results = response.json()["data"]
        assert list(results.keys()) == ["uuid1"]
        assert len(results["uuid1"]) == 1
        results = [V1Events.read(**i) for i in response.json()["data"]["uuid1"]]
        assert results[0].name == events11.name
        assert results[0].kind == events11.kind
        assert pd.DataFrame.equals(results[0].df, events11.df)

        response = self.client.get(
            self.base_url + "/metric?names=metric1,metric2&runs=uuid1,uuid2&orient=csv"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True
        events12 = V1Events.read(
            name="metric2", kind=V1ArtifactKind.METRIC, data=filepath12
        )
        events21 = V1Events.read(
            name="metric1", kind=V1ArtifactKind.METRIC, data=filepath21
        )
        events22 = V1Events.read(
            name="metric2", kind=V1ArtifactKind.METRIC, data=filepath22
        )
        expected = {
            "uuid1": {events11.name: events11, events12.name: events12},
            "uuid2": {events21.name: events21, events22.name: events22},
        }
        response = response.json()["data"]
        results = {
            run_uuid: [V1Events.read(**i) for i in response[run_uuid]]
            for run_uuid in response
        }
        for run_uuid in results:
            for res in results[run_uuid]:
                exp = expected[run_uuid][res.name]
                assert res.name == exp.name
                assert res.kind == exp.kind
                assert pd.DataFrame.equals(res.df, exp.df)

        response = self.client.get(
            self.base_url
            + "/metric?names=metric12,text2,text3&runs=uuid1,uuid2,uuid3&orient=csv"
        )
        assert response.status_code == 200
        assert os.path.exists(filepath11) is True
        assert os.path.exists(filepath12) is True
        assert os.path.exists(filepath21) is True
        assert os.path.exists(filepath22) is True
        expected = {
            "uuid1": {events11.name: events11, events12.name: events12},
            "uuid2": {events21.name: events21, events22.name: events22},
        }
        response = response.json()["data"]
        results = {
            run_uuid: [V1Events.read(**i) for i in response[run_uuid]]
            for run_uuid in response
        }
        for run_uuid in results:
            for res in results[run_uuid]:
                exp = expected[run_uuid][res.name]
                assert res.name == exp.name
                assert res.kind == exp.kind
                assert pd.DataFrame.equals(res.df, exp.df)
