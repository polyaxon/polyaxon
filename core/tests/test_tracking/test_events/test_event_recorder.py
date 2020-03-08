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
import tempfile

import pytest

from tests.utils import BaseTestCase

from polyaxon.polyboard.events.schemas import (
    LoggedEventListSpec,
    LoggedEventSpec,
    V1Event,
    V1Events,
)
from polyaxon.tracking.events.writer import (
    EventAsyncManager,
    EventFileWriter,
    EventWriter,
)


@pytest.mark.tracking_mark
class TestEventWriter(BaseTestCase):
    def test_event_file(self):
        run_path = tempfile.mkdtemp()
        ew = EventWriter(run_path=run_path, backend=EventWriter.EVENTS_BACKEND)
        assert ew._get_event_path(
            kind="kind", name="name"
        ) == "{}/events/kind/name.plx".format(run_path)

    def test_init_events(self):
        events = LoggedEventListSpec(name="test", kind="metric", events=[])

        run_path = tempfile.mkdtemp()
        ew = EventWriter(run_path=run_path, backend=EventWriter.EVENTS_BACKEND)

        event_file = ew._get_event_path(name=events.name, kind=events.kind)

        assert os.path.exists(event_file) is False
        ew._init_events(events)
        assert os.path.exists(event_file) is True
        expected_events = V1Events.read(kind="metric", name="test", data=event_file)
        assert expected_events.name == events.name
        assert expected_events.kind == events.kind

        # Init same file
        ew._init_events(events)
        assert os.path.exists(event_file) is True

        # New file
        events = LoggedEventListSpec(name="new", kind="text", events=[])

        new_event_file = ew._get_event_path(name=events.name, kind=events.kind)

        assert os.path.exists(new_event_file) is False
        ew._init_events(events)
        assert os.path.exists(new_event_file) is True
        expected_events = V1Events.read(kind="text", name="new", data=new_event_file)
        assert expected_events.name == events.name
        assert expected_events.kind == events.kind

        # Previous file should still be there
        assert os.path.exists(event_file) is True

    def test_add_event_create_files_and_batch_events(self):
        run_path = tempfile.mkdtemp()
        ew = EventWriter(run_path=run_path, backend=EventWriter.EVENTS_BACKEND)
        events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=1, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=2, metric=1.13)
            ),
            LoggedEventSpec(
                name="test2", kind="metric", event=V1Event.make(step=2, metric=1.13)
            ),
            LoggedEventSpec(
                name="test", kind="text", event=V1Event.make(step=1, text="text")
            ),
            LoggedEventSpec(
                name="test", kind="html", event=V1Event.make(step=1, html="html")
            ),
        ]
        ew.write(events)
        for event in events:
            new_event_file = ew._get_event_path(kind=event.kind, name=event.name)
            assert os.path.exists(new_event_file) is True

        assert len(os.listdir(run_path + "/events")) == 3

        # Check the queues
        assert len(ew._files) == 4
        assert ew._files["metric.test"].name == "test"
        assert ew._files["metric.test"].kind == "metric"
        assert [e.to_dict() for e in ew._files["metric.test"].events] == [
            events[0].event.to_dict(),
            events[1].event.to_dict(),
        ]

        assert ew._files["metric.test2"].name == "test2"
        assert ew._files["metric.test2"].kind == "metric"
        assert [e.to_dict() for e in ew._files["metric.test2"].events] == [
            events[2].event.to_dict()
        ]

        assert ew._files["text.test"].name == "test"
        assert ew._files["text.test"].kind == "text"
        assert [e.to_dict() for e in ew._files["text.test"].events] == [
            events[3].event.to_dict()
        ]

        assert ew._files["html.test"].name == "test"
        assert ew._files["html.test"].kind == "html"
        assert [e.to_dict() for e in ew._files["html.test"].events] == [
            events[4].event.to_dict()
        ]

    def test_expect_closing_flushes_data_to_files(self):
        run_path = tempfile.mkdtemp()
        ew = EventWriter(run_path=run_path, backend=EventWriter.EVENTS_BACKEND)
        events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=1, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=12, metric=1.12)
            ),
        ]
        ew.write(events)
        ew.close()

        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1

        results = V1Events.read(
            name="test",
            kind="metric",
            data=ew._get_event_path(kind="metric", name="test"),
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 2
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()

        # all flushed
        assert ew._files["metric.test"].events == []

        # Adding more events
        new_events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=14, metric=1.12)
            ),
            LoggedEventSpec(
                name="test2", kind="metric", event=V1Event.make(step=14, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="html", event=V1Event.make(step=12, html="some div")
            ),
        ]
        ew.write(new_events)
        ew.close()

        assert len(os.listdir(run_path + "/events")) == 2  # metric and html
        assert len(os.listdir(run_path + "/events/metric")) == 2

        results = V1Events.read(
            name="test",
            kind="metric",
            data=ew._get_event_path(kind="metric", name="test"),
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 4
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()
        assert results.get_event_at(2).to_dict() == new_events[0].event.to_dict()
        assert results.get_event_at(3).to_dict() == new_events[1].event.to_dict()


@pytest.mark.tracking_mark
class TestEventFileWriter(BaseTestCase):
    def test_event_file_writer_initializes_paths(self):
        some_path = tempfile.mkdtemp()
        assert os.path.exists(some_path + "/run_uid") is False
        EventFileWriter(some_path + "/run_uid")
        assert os.path.exists(some_path + "/run_uid") is True
        assert os.path.exists(some_path + "/run_uid/events") is True
        assert os.path.exists(some_path + "/run_uid/assets") is True

    def test_event_file_writer(self):
        run_path = tempfile.mkdtemp()
        ew = EventFileWriter(run_path)
        events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=1, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=12, metric=1.12)
            ),
        ]
        for e in events:
            ew.add_event(e)
        ew.flush()
        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 2
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()

        # Adding more events
        new_events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=14, metric=1.12)
            ),
            LoggedEventSpec(
                name="test2", kind="metric", event=V1Event.make(step=14, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="html", event=V1Event.make(step=12, html="some div")
            ),
        ]
        for e in new_events:
            ew.add_event(e)
        ew.flush()

        assert len(os.listdir(run_path + "/events")) == 2  # metric and html
        assert len(os.listdir(run_path + "/events/metric")) == 2

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 4
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()
        assert results.get_event_at(2).to_dict() == new_events[0].event.to_dict()
        assert results.get_event_at(3).to_dict() == new_events[1].event.to_dict()

    def test_write_batch_events_file_writer(self):
        run_path = tempfile.mkdtemp()
        ew = EventFileWriter(run_path)
        events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=1, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=12, metric=1.12)
            ),
        ]
        ew.add_events(events)
        ew.flush()
        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 2
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()

    def test_event_file_writer_append_after_close_reopen(self):
        run_path = tempfile.mkdtemp()
        ew = EventFileWriter(run_path)
        events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=1, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=12, metric=1.12)
            ),
        ]
        for e in events:
            ew.add_event(e)
        ew.close()
        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 2
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()

        # New writer should resume work
        ew = EventFileWriter(run_path)
        # Adding more events
        new_events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=14, metric=1.12)
            ),
            LoggedEventSpec(
                name="test2", kind="metric", event=V1Event.make(step=14, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="html", event=V1Event.make(step=12, html="some div")
            ),
        ]
        for e in new_events:
            ew.add_event(e)
        ew.close()

        assert len(os.listdir(run_path + "/events")) == 2  # metric and html
        assert len(os.listdir(run_path + "/events/metric")) == 2

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 4
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()
        assert results.get_event_at(2).to_dict() == new_events[0].event.to_dict()
        assert results.get_event_at(3).to_dict() == new_events[1].event.to_dict()

    def test_event_file_writer_raise_after_close(self):
        run_path = tempfile.mkdtemp()
        ew = EventFileWriter(run_path)
        events = [
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=1, metric=1.12)
            ),
            LoggedEventSpec(
                name="test", kind="metric", event=V1Event.make(step=12, metric=1.12)
            ),
        ]
        for e in events:
            ew.add_event(e)
        ew.close()
        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 2
        assert results.get_event_at(0).to_dict() == events[0].event.to_dict()
        assert results.get_event_at(1).to_dict() == events[1].event.to_dict()

        # Adding event raises
        with self.assertRaises(OSError):
            ew.add_event(
                LoggedEventSpec(
                    name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
                )
            )

    def test_async_writer_without_write(self):
        run_path = tempfile.mkdtemp()
        ew = EventFileWriter(run_path)
        ew.close()
        assert len(os.listdir(run_path + "/events")) == 0


@pytest.mark.tracking_mark
class TestEventAsyncManager(BaseTestCase):
    def test_async_writer_write_once(self):
        run_path = tempfile.mkdtemp()
        ew = EventAsyncManager(
            event_writer=EventWriter(run_path, backend=EventWriter.EVENTS_BACKEND)
        )
        event = LoggedEventSpec(
            name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
        )
        ew.write(event)
        ew.close()
        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1
        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 1
        assert results.get_event_at(0).to_dict() == event.event.to_dict()

    def test_async_writer_write_queue_full(self):
        run_path = tempfile.mkdtemp()
        ew = EventAsyncManager(
            event_writer=EventWriter(run_path, backend=EventWriter.EVENTS_BACKEND)
        )
        event = LoggedEventSpec(
            name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
        )
        repeat = 100
        for i in range(repeat):
            ew.write(event)
        ew.close()

        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1

        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 100
        assert results.get_event_at(0).to_dict() == event.event.to_dict()

    def test_async_writer_write_one_slot_queue(self):
        run_path = tempfile.mkdtemp()
        ew = EventAsyncManager(
            event_writer=EventWriter(run_path, backend=EventWriter.EVENTS_BACKEND),
            max_queue_size=1,
        )
        event = LoggedEventSpec(
            name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
        )
        repeat = 10
        for i in range(repeat):
            ew.write(event)
        ew.close()

        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1
        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 10
        assert results.get_event_at(0).to_dict() == event.event.to_dict()

    def test_async_writer_close_triggers_flush(self):
        run_path = tempfile.mkdtemp()
        ew = EventAsyncManager(
            event_writer=EventWriter(run_path, backend=EventWriter.EVENTS_BACKEND),
            max_queue_size=1,
        )
        event = LoggedEventSpec(
            name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
        )
        ew.write(event)
        ew.close()

        assert len(os.listdir(run_path + "/events")) == 1
        assert len(os.listdir(run_path + "/events/metric")) == 1
        results = V1Events.read(
            name="test", kind="metric", data=run_path + "/events/metric/test.plx"
        )
        assert results.name == "test"
        assert results.kind == "metric"
        assert len(results.df.values) == 1
        assert results.get_event_at(0).to_dict() == event.event.to_dict()

    def test_write_after_async_writer_closed(self):
        run_path = tempfile.mkdtemp()
        ew = EventAsyncManager(
            event_writer=EventWriter(run_path, backend=EventWriter.EVENTS_BACKEND),
            max_queue_size=1,
        )
        event = LoggedEventSpec(
            name="test", kind="metric", event=V1Event.make(step=13, metric=1.12)
        )
        ew.close()

        with self.assertRaises(IOError):
            ew.write(event)

        # nothing is written to the file after close
        assert len(os.listdir(run_path)) == 0
