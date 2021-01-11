#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import pytest

from dateutil import parser as dt_parser

from polyaxon.polyboard.logging.schemas import V1Log, V1Logs
from polyaxon.utils.tz_utils import now
from tests.utils import BaseTestCase


@pytest.mark.polyboard_mark
class TestLogV1(BaseTestCase):
    def test_has_timestamp(self):
        parsed = V1Log.process_log_line(
            value="foo",
            timestamp="2018-12-11 10:24:57 UTC",
            node="node1",
            pod="pod1",
            container="container1",
        )
        expected = V1Log(
            value="foo",
            timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
            node="node1",
            pod="pod1",
            container="container1",
        )
        assert parsed == expected

    def test_has_no_timestamp(self):
        log_result = V1Log.process_log_line(
            value="foo", node="node1", pod="pod1", container="container1"
        )
        assert log_result.timestamp.date() == now().date()

    def test_has_datetime_timestamp(self):
        log_result = V1Log.process_log_line(
            timestamp=now(),
            value="foo",
            node="node1",
            pod="pod1",
            container="container1",
        )
        assert log_result.timestamp.date() == now().date()

    def test_log_line_has_datetime(self):
        parsed = V1Log.process_log_line(
            value="2018-12-11 10:24:57 UTC foo",
            node="node1",
            pod="pod1",
            container="container1",
        )
        expected = V1Log(
            value="foo",
            timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
            node="node1",
            pod="pod1",
            container="container1",
        )
        assert parsed == expected

    def test_log_line_has_iso_datetime(self):
        parsed = V1Log.process_log_line(
            value="2018-12-11T08:49:07.163495183Z foo",
            node="node1",
            pod="pod1",
            container="container1",
        )
        expected = V1Log(
            value="foo",
            timestamp=dt_parser.parse("2018-12-11T08:49:07.163495+00:00"),
            node="node1",
            pod="pod1",
            container="container1",
        )
        assert parsed == expected


class TestLogsV1(BaseTestCase):
    def test_logs(self):
        logs = V1Logs(
            last_file=1000,
            logs=[
                V1Log(
                    value="foo",
                    timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                    node="node1",
                    pod="pod1",
                    container="container1",
                ),
                V1Log(
                    value="foo",
                    timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                    node="node1",
                    pod="pod1",
                    container="container1",
                ),
                V1Log(
                    value="foo",
                    timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                    node="node1",
                    pod="pod1",
                    container="container1",
                ),
            ],
        )
        logs_dict = logs.to_light_dict()
        assert logs_dict == logs.from_dict(logs_dict).to_light_dict()
        assert logs_dict == logs.read(logs.to_dict(dump=True)).to_light_dict()

    def test_logs_with_files(self):
        logs = V1Logs(
            last_file=1000,
            last_time=now(),
            files=["file1", "file2"],
            logs=[
                V1Log(
                    value="foo",
                    timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                    node="node1",
                    pod="pod1",
                    container="container1",
                ),
                V1Log(
                    value="foo",
                    timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                    node="node1",
                    pod="pod1",
                    container="container1",
                ),
                V1Log(
                    value="foo",
                    timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                    node="node1",
                    pod="pod1",
                    container="container1",
                ),
            ],
        )
        logs_dict = logs.to_light_dict()
        assert logs_dict == logs.from_dict(logs_dict).to_light_dict()
        assert logs_dict == logs.read(logs.to_dict(dump=True)).to_light_dict()

    def test_chunk_logs(self):
        logs = [
            V1Log(
                value="foo1",
                timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                node="node1",
                pod="pod1",
                container="container1",
            ),
            V1Log(
                value="foo2",
                timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                node="node1",
                pod="pod1",
                container="container1",
            ),
            V1Log(
                value="foo3",
                timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"),
                node="node1",
                pod="pod1",
                container="container1",
            ),
        ]

        V1Logs.CHUNK_SIZE = 2
        chunks = [c for c in V1Logs.chunk_logs(logs)]
        # 1 chunk
        assert [i.value for i in chunks[0].logs] == ["foo1", "foo2"]

        # 2 chunk
        assert [i.value for i in chunks[1].logs] == ["foo3"]
