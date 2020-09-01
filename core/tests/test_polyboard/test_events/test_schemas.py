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

import pytest

from dateutil import parser as dt_parser
from tests.utils import BaseTestCase

from polyaxon.polyboard.events import (
    V1Event,
    V1EventArtifact,
    V1EventAudio,
    V1EventChart,
    V1EventHistogram,
    V1EventImage,
    V1EventModel,
    V1Events,
)
from polyaxon.polyboard.events.schemas import (
    LoggedEventListSpec,
    V1EventCurve,
    V1EventDataframe,
    V1EventVideo,
)
from polyaxon.utils.tz_utils import now


@pytest.mark.polyboard_mark
class TestBaseEvent(BaseTestCase):
    def test_has_timestamp(self):
        parsed = V1Event.make(timestamp="2018-12-11 10:24:57 UTC")
        expected = V1Event(timestamp=dt_parser.parse("2018-12-11 10:24:57 UTC"))
        assert parsed == expected

    def test_has_no_timestamp(self):
        event_result = V1Event.make()
        assert event_result.timestamp.date() == now().date()

    def test_has_datetime_timestamp(self):
        event_result = V1Event.make(timestamp=now())
        assert event_result.timestamp.date() == now().date()

    def test_log_line_has_datetime(self):
        parsed = V1Event.make(timestamp="2018-12-11 10:24:57", step=12)
        expected = V1Event(timestamp=dt_parser.parse("2018-12-11 10:24:57"), step=12)
        assert parsed == expected

    def test_log_line_has_iso_datetime(self):
        parsed = V1Event.make(timestamp="2018-12-11T08:49:07.163495183Z", step=12)
        expected = V1Event(
            timestamp=dt_parser.parse("2018-12-11T08:49:07.163495+00:00"), step=12
        )
        assert parsed == expected


class TestEventsV1(BaseTestCase):
    def test_metrics(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="metric",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    metric=0.1,
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    metric=0.112,
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    metric=0.1,
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_metrics_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"), metric=0.1, step=12
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"), metric=0.2, step=13
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"), metric=0.3, step=14
            ),
        ]
        events = V1Events.read(
            name="metric_events",
            kind="metric",
            data=os.path.abspath("tests/fixtures/polyboard/metric/metric_events.plx"),
        )
        assert events.name == "metric_events"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_images(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="metric",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    image=V1EventImage(height=1, width=1, colorspace=1, path="path"),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    image=V1EventImage(height=10, width=1, colorspace=0, path="path"),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    image=V1EventImage(height=1, width=10, colorspace=2, path="path"),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_images_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                image=V1EventImage(path="test"),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                image=V1EventImage(height=1, width=1),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                image=V1EventImage(height=10, width=10, colorspace=2),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="image",
            data=os.path.abspath("tests/fixtures/polyboard/image/image_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_histogram(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="histogram",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    histogram=V1EventHistogram(values=[10], counts=[1]),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    histogram=V1EventHistogram(values=[10], counts=[1]),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    histogram=V1EventHistogram(values=[10], counts=[1]),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_histograms_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                histogram=V1EventHistogram(values=[10], counts=[1]),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                histogram=V1EventHistogram(values=[10, 1, 1], counts=[1, 1, 1]),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                histogram=V1EventHistogram(
                    values=[10, 112, 12, 1], counts=[12, 1, 1, 1]
                ),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="histogram",
            data=os.path.abspath(
                "tests/fixtures/polyboard/histogram/histogram_events.plx"
            ),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_video(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="video",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    video=V1EventVideo(height=1, width=1, colorspace=1, path="path"),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    video=V1EventVideo(height=10, width=1, colorspace=0, path="path"),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    video=V1EventVideo(height=1, width=10, colorspace=2, path="path"),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_videos_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                video=V1EventVideo(path="test", content_type="mp4"),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                video=V1EventVideo(height=1, width=1),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                video=V1EventVideo(height=10, width=10, colorspace=2),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="video",
            data=os.path.abspath("tests/fixtures/polyboard/video/video_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_audio(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="audio",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    audio=V1EventAudio(
                        sample_rate=1.1, num_channels=2, length_frames=2, path="test"
                    ),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    audio=V1EventAudio(
                        sample_rate=1.1, num_channels=2, length_frames=2, path="test"
                    ),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    audio=V1EventAudio(
                        sample_rate=1.12, num_channels=22, length_frames=22, path="test"
                    ),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_audios_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                audio=V1EventAudio(
                    sample_rate=1.1, num_channels=2, length_frames=2, path="test"
                ),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                audio=V1EventAudio(
                    sample_rate=1.11,
                    num_channels=22,
                    length_frames=22,
                    path="test",
                    content_type="wav",
                ),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                audio=V1EventAudio(path="testwave", content_type="wav"),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="audio",
            data=os.path.abspath("tests/fixtures/polyboard/audio/audio_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_html(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="html",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    html="<div>1</div>",
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    html="<div>2</div>",
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    html="<div>3</div>",
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_htmls_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                html="<div>1</div>",
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                html="<div>2</div>",
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                html="<div>3</div>",
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="html",
            data=os.path.abspath("tests/fixtures/polyboard/html/html_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_chart(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="chart",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    chart=V1EventChart(kind="plotly", figure={"foo": "bar"}),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    chart=V1EventChart(kind="vega", figure={"foo": "bar"}),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    chart=V1EventChart(kind="bokeh", figure={"foo": "bar"}),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_charts_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                chart=V1EventChart(kind="plotly", figure={"foo": "bar"}),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                chart=V1EventChart(kind="vega", figure={"foo2": "bar2"}),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                chart=V1EventChart(kind="bokeh", figure={"foo3": "bar3"}),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="chart",
            data=os.path.abspath("tests/fixtures/polyboard/chart/chart_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_curve(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="curve",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    curve=V1EventCurve(
                        kind="roc",
                        x=[1.1, 3.1, 5.1],
                        y=[0.1, 0.3, 0.4],
                        annotation="0.1",
                    ),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    curve=V1EventCurve(
                        kind="pr",
                        x=[1.1, 3.1, 5.1],
                        y=[0.1, 0.3, 0.4],
                        annotation="0.21",
                    ),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    curve=V1EventCurve(
                        kind="custom",
                        x=[1.1, 3.1, 5.1],
                        y=[0.1, 0.3, 0.4],
                        annotation="0.1",
                    ),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_curves_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                curve=V1EventCurve(
                    kind="roc", x=[1.1, 3.1, 5.1], y=[0.1, 0.3, 0.4], annotation="0.1"
                ),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                curve=V1EventCurve(
                    kind="pr", x=[1.1, 3.1, 5.1], y=[0.1, 0.3, 0.4], annotation="0.21"
                ),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                curve=V1EventCurve(
                    kind="custom",
                    x=[1.1, 3.1, 5.1],
                    y=[0.1, 0.3, 0.4],
                    annotation="0.1",
                ),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="curve",
            data=os.path.abspath("tests/fixtures/polyboard/curve/curve_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_artifact(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="artifact",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    artifact=V1EventArtifact(kind="dataframe", path="path"),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    artifact=V1EventArtifact(kind="tsv", path="path"),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    artifact=V1EventArtifact(kind="csv", path="path"),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_artifacts_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                artifact=V1EventArtifact(kind="dataframe", path="path1"),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                artifact=V1EventArtifact(kind="tsv", path="path2"),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                artifact=V1EventArtifact(kind="csv", path="path3"),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="artifact",
            data=os.path.abspath(
                "tests/fixtures/polyboard/artifact/artifact_events.plx"
            ),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

    def test_model(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="model",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    model=V1EventModel(framework="tensorflow", path="path"),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    model=V1EventModel(framework="pytorch", path="path"),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    model=V1EventModel(framework="onnx", path="path"),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_models_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                model=V1EventModel(framework="tensorflow", path="path1"),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                model=V1EventModel(framework="pytorch", path="path2"),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                model=V1EventModel(framework="onnx", path="path3"),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="model",
            data=os.path.abspath("tests/fixtures/polyboard/model/model_events.plx"),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()

        # Test single event
        events = V1Events.read(
            name="foo",
            kind="model",
            data=os.path.abspath(
                "tests/fixtures/polyboard/model/model_events_without_step.plx"
            ),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 1
        event = V1Event(
            timestamp=dt_parser.parse("2018-12-11 10:24:57"),
            model=V1EventModel(framework="tensorflow", path="path1"),
        )
        events.get_event_at(0).to_dict()
        assert events.get_event_at(0).to_dict() == event.to_dict()

    def test_dataframe(self):
        events = LoggedEventListSpec(
            name="foo",
            kind="dataframe",
            events=[
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                    dataframe=V1EventDataframe(path="path", content_type="parquet"),
                    step=12,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 11:24:57"),
                    dataframe=V1EventDataframe(path="path", content_type="pickle"),
                    step=13,
                ),
                V1Event(
                    timestamp=dt_parser.parse("2018-12-11 12:24:57"),
                    dataframe=V1EventDataframe(path="path"),
                    step=14,
                ),
            ],
        )
        events_dict = events.to_dict()
        assert events_dict == events.from_dict(events_dict).to_dict()

    def test_dataframes_read_yaml(self):
        values = [
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:24:57"),
                dataframe=V1EventDataframe(path="path1", content_type="parquet"),
                step=12,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:25:57"),
                dataframe=V1EventDataframe(path="path2", content_type="pickle"),
                step=13,
            ),
            V1Event(
                timestamp=dt_parser.parse("2018-12-11 10:26:57"),
                dataframe=V1EventDataframe(path="path3"),
                step=14,
            ),
        ]
        events = V1Events.read(
            name="foo",
            kind="dataframe",
            data=os.path.abspath(
                "tests/fixtures/polyboard/dataframe/dataframe_events.plx"
            ),
        )
        assert events.name == "foo"
        assert len(events.df.values) == 3
        for i in range(3):
            assert events.get_event_at(i).to_dict() == values[i].to_dict()
