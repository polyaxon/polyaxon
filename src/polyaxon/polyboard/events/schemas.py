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
import json

from collections import namedtuple
from typing import Dict, Mapping, Optional, Union

import polyaxon_sdk

from marshmallow import ValidationError, fields, pre_load, validate, validates_schema

from polyaxon.parser import parser
from polyaxon.polyboard.artifacts.kinds import V1ArtifactKind
from polyaxon.polyboard.utils import validate_csv
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.utils.date_utils import parse_datetime
from polyaxon.utils.np_utils import sanitize_np_types
from polyaxon.utils.signal_decorators import check_partial
from polyaxon.utils.tz_utils import now


class EventImageSchema(BaseSchema):
    height = fields.Int(allow_none=True)
    width = fields.Int(allow_none=True)
    colorspace = fields.Int(allow_none=True)
    path = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventImage


class V1EventImage(BaseConfig, polyaxon_sdk.V1EventImage):
    IDENTIFIER = "image"
    SCHEMA = EventImageSchema
    REDUCED_ATTRIBUTES = ["height", "width", "colorspace", "path"]


class EventVideoSchema(BaseSchema):
    height = fields.Int(allow_none=True)
    width = fields.Int(allow_none=True)
    colorspace = fields.Int(allow_none=True)
    path = fields.Str(allow_none=True)
    content_type = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventVideo


class V1EventVideo(BaseConfig, polyaxon_sdk.V1EventVideo):
    IDENTIFIER = "video"
    SCHEMA = EventImageSchema
    REDUCED_ATTRIBUTES = ["height", "width", "colorspace", "path", "content_type"]


class EventDataframeSchema(BaseSchema):
    path = fields.Str(allow_none=True)
    content_type = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventDataframe


class V1EventDataframe(BaseConfig, polyaxon_sdk.V1EventDataframe):
    IDENTIFIER = "dataframe"
    SCHEMA = EventDataframeSchema
    REDUCED_ATTRIBUTES = ["path", "content_type"]


class EventHistogramSchema(BaseSchema):
    values = fields.List(fields.Float(), allow_none=True)
    counts = fields.List(fields.Float(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventHistogram


class V1EventHistogram(BaseConfig, polyaxon_sdk.V1EventHistogram):
    IDENTIFIER = "histogram"
    SCHEMA = EventHistogramSchema
    REDUCED_ATTRIBUTES = ["values", "counts"]


class EventAudioSchema(BaseSchema):
    sample_rate = fields.Float(allow_none=True)
    num_channels = fields.Int(allow_none=True)
    length_frames = fields.Int(allow_none=True)
    path = fields.Str(allow_none=True)
    content_type = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventAudio


class V1EventAudio(BaseConfig, polyaxon_sdk.V1EventAudio):
    IDENTIFIER = "audio"
    SCHEMA = EventAudioSchema
    REDUCED_ATTRIBUTES = [
        "sample_rate",
        "num_channels",
        "length_frames",
        "path",
        "content_type",
    ]


class V1EventChartKind(polyaxon_sdk.V1EventChartKind):
    pass


class EventChartSchema(BaseSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.OneOf(V1EventChartKind.allowable_values)
    )
    figure = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventChart


class V1EventChart(BaseConfig, polyaxon_sdk.V1EventChart):
    IDENTIFIER = "chart"
    SCHEMA = EventChartSchema
    REDUCED_ATTRIBUTES = ["kind", "figure"]

    def to_dict(self, humanize_values=False, unknown=None, dump=False):
        if self.kind == V1EventChartKind.PLOTLY:
            import plotly.tools

            obj = self.obj_to_dict(
                self, humanize_values=humanize_values, unknown=unknown
            )
            return json.dumps(obj, cls=plotly.utils.PlotlyJSONEncoder)
        # Resume normal serialization
        return super().to_dict(humanize_values, unknown, dump)


class V1EventCurveKind(polyaxon_sdk.V1EventCurveKind):
    pass


class EventCurveSchema(BaseSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.OneOf(V1EventCurveKind.allowable_values)
    )
    x = fields.List(fields.Float(), allow_none=True)
    y = fields.List(fields.Float(), allow_none=True)
    annotation = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventCurve


class V1EventCurve(BaseConfig, polyaxon_sdk.V1EventCurve):
    IDENTIFIER = "curve"
    SCHEMA = EventCurveSchema
    REDUCED_ATTRIBUTES = ["kind", "x", "y", "annotation"]


class EventArtifactSchema(BaseSchema):
    kind = fields.Str(
        allow_none=True, validate=validate.OneOf(V1ArtifactKind.allowable_values)
    )
    path = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventArtifact


class V1EventArtifact(BaseConfig, polyaxon_sdk.V1EventArtifact):
    IDENTIFIER = "artifact"
    SCHEMA = EventArtifactSchema
    REDUCED_ATTRIBUTES = ["kind", "path"]


class EventModelSchema(BaseSchema):
    framework = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    spec = fields.Raw(allow_none=True)

    @staticmethod
    def schema_config():
        return V1EventModel


class V1EventModel(BaseConfig, polyaxon_sdk.V1EventModel):
    IDENTIFIER = "artifact"
    SCHEMA = EventModelSchema
    REDUCED_ATTRIBUTES = ["framework", "path", "spec"]


class EventSchema(BaseSchema):
    timestamp = fields.DateTime(allow_none=True)
    step = fields.Int(allow_none=True)
    metric = fields.Float(allow_none=True)
    image = fields.Nested(EventImageSchema, allow_none=True)
    histogram = fields.Nested(EventHistogramSchema, allow_none=True)
    audio = fields.Nested(EventAudioSchema, allow_none=True)
    video = fields.Nested(EventVideoSchema, allow_none=True)
    html = fields.Str(allow_none=True)
    text = fields.Str(allow_none=True)
    chart = fields.Nested(EventChartSchema, allow_none=True)
    curve = fields.Nested(EventCurveSchema, allow_none=True)
    artifact = fields.Nested(EventArtifactSchema, allow_none=True)
    model = fields.Nested(EventModelSchema, allow_none=True)
    dataframe = fields.Nested(EventDataframeSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Event

    @pre_load
    def pre_validate(self, data, **kwargs):
        if data.get("image") is not None:
            data["image"] = parser.get_dict(
                key="image",
                value=data["image"],
            )
        if data.get("histogram") is not None:
            data["histogram"] = parser.get_dict(
                key="histogram",
                value=data["histogram"],
            )
        if data.get("audio") is not None:
            data["audio"] = parser.get_dict(
                key="audio",
                value=data["audio"],
            )
        if data.get("video") is not None:
            data["video"] = parser.get_dict(
                key="video",
                value=data["video"],
            )
        if data.get("chart") is not None:
            data["chart"] = parser.get_dict(
                key="chart",
                value=data["chart"],
            )
        if data.get("curve") is not None:
            data["curve"] = parser.get_dict(
                key="curve",
                value=data["curve"],
            )
        if data.get("artifact") is not None:
            data["artifact"] = parser.get_dict(
                key="artifact",
                value=data["artifact"],
            )
        if data.get("model") is not None:
            data["model"] = parser.get_dict(
                key="model",
                value=data["model"],
            )
        if data.get("dataframe") is not None:
            data["dataframe"] = parser.get_dict(
                key="dataframe",
                value=data["dataframe"],
            )

        return data

    @validates_schema
    @check_partial
    def validate_event(self, values, **kwargs):
        count = 0

        def increment(c):
            c += 1
            if c > 1:
                raise ValidationError(
                    "An event should have one and only one primitive, found {}.".format(
                        c
                    )
                )
            return c

        if values.get("metric") is not None:
            count = increment(count)
        if values.get("image") is not None:
            count = increment(count)
        if values.get("histogram") is not None:
            count = increment(count)
        if values.get("audio") is not None:
            count = increment(count)
        if values.get("video") is not None:
            count = increment(count)
        if values.get("html") is not None:
            count = increment(count)
        if values.get("text") is not None:
            count = increment(count)
        if values.get("chart") is not None:
            count = increment(count)
        if values.get("curve") is not None:
            count = increment(count)
        if values.get("artifact") is not None:
            count = increment(count)
        if values.get("model") is not None:
            count = increment(count)
        if values.get("dataframe") is not None:
            count = increment(count)

        if count != 1:
            raise ValidationError(
                "An event should have one and only one primitive, found {}.".format(
                    count
                )
            )


class V1Event(BaseConfig, polyaxon_sdk.V1Event):
    SEPARATOR = "|"
    IDENTIFIER = "event"
    SCHEMA = EventSchema
    REDUCED_ATTRIBUTES = [
        "metric",
        "image",
        "histogram",
        "audio",
        "video",
        "html",
        "text",
        "chart",
        "curve",
        "artifact",
        "model",
        "dataframe",
    ]

    @classmethod
    def make(
        cls,
        step: int = None,
        timestamp=None,
        metric: float = None,
        image: V1EventImage = None,
        histogram: V1EventHistogram = None,
        audio: V1EventAudio = None,
        video: V1EventVideo = None,
        html: str = None,
        text: str = None,
        chart: V1EventChart = None,
        curve: V1EventCurve = None,
        artifact: V1EventArtifact = None,
        model: V1EventModel = None,
        dataframe: V1EventDataframe = None,
    ) -> "V1Event":
        if isinstance(timestamp, str):
            try:
                timestamp = parse_datetime(timestamp)
            except Exception as e:
                raise ValidationError("Received an invalid timestamp") from e

        return cls(
            timestamp=timestamp if timestamp else now(tzinfo=True),
            step=step,
            metric=metric,
            image=image,
            histogram=histogram,
            audio=audio,
            video=video,
            html=html,
            text=text,
            chart=chart,
            curve=curve,
            artifact=artifact,
            model=model,
            dataframe=dataframe,
        )

    def get_value(self, dump=True):
        if self.metric is not None:
            return str(self.metric) if dump else self.metric
        if self.image is not None:
            return self.image.to_dict(dump=dump) if dump else self.image
        if self.histogram is not None:
            return self.histogram.to_dict(dump=dump) if dump else self.histogram
        if self.audio is not None:
            return self.audio.to_dict(dump=dump) if dump else self.audio
        if self.video is not None:
            return self.video.to_dict(dump=dump) if dump else self.video
        if self.html is not None:
            return self.html
        if self.text is not None:
            return self.text
        if self.chart is not None:
            return self.chart.to_dict(dump=dump) if dump else self.chart
        if self.curve is not None:
            return self.curve.to_dict(dump=dump) if dump else self.curve
        if self.artifact is not None:
            return self.artifact.to_dict(dump=dump) if dump else self.artifact
        if self.model is not None:
            return self.model.to_dict(dump=dump) if dump else self.model
        if self.dataframe is not None:
            return self.dataframe.to_dict(dump=dump) if dump else self.dataframe

    def to_csv(self) -> str:
        values = [
            str(self.step) if self.step is not None else "",
            str(self.timestamp) if self.timestamp is not None else "",
            self.get_value(dump=True),
        ]

        return self.SEPARATOR.join(values)


class V1Events:
    ORIENT_CSV = "csv"
    ORIENT_DICT = "dict"

    def __init__(self, kind, name, df):
        self.kind = kind
        self.name = name
        self.df = df

    @classmethod
    def read(
        cls, kind: str, name: str, data: Union[str, Dict], parse_dates: bool = True
    ) -> "V1Events":
        import pandas as pd

        if isinstance(data, str):
            csv = validate_csv(data)
            if parse_dates:
                df = pd.read_csv(
                    csv,
                    sep=V1Event.SEPARATOR,
                    parse_dates=["timestamp"],
                )
            else:
                df = pd.read_csv(
                    csv,
                    sep=V1Event.SEPARATOR,
                )
        elif isinstance(data, dict):
            df = pd.DataFrame.from_dict(data)
        else:
            raise ValueError(
                "V1Events received an unsupported value type: {}".format(type(data))
            )

        return cls(name=name, kind=kind, df=df)

    def to_dict(self, orient: str = "list") -> Dict:
        import numpy as np

        return self.df.replace({np.nan: None}).to_dict(orient=orient)

    def get_event_at(self, index):
        event = self.df.iloc[index].to_dict()
        event["timestamp"] = event["timestamp"].isoformat()
        event["step"] = sanitize_np_types(event["step"])
        return V1Event.from_dict(event)

    def _get_step_summary(self) -> Optional[Dict]:
        _count = self.df.step.count()
        if _count == 0:
            return None

        return {
            "count": sanitize_np_types(_count),
            "min": sanitize_np_types(self.df.step.iloc[0]),
            "max": sanitize_np_types(self.df.step.iloc[-1]),
        }

    def _get_ts_summary(self) -> Optional[Dict]:
        _count = self.df.timestamp.count()
        if _count == 0:
            return None

        return {
            "min": self.df.timestamp.iloc[0].isoformat(),
            "max": self.df.timestamp.iloc[-1].isoformat(),
        }

    def get_summary(self) -> Dict:
        summary = {"is_event": True}
        step_summary = self._get_step_summary()
        if step_summary:
            summary["step"] = step_summary

        ts_summary = self._get_ts_summary()
        if ts_summary:
            summary["timestamp"] = ts_summary

        if self.kind == V1ArtifactKind.METRIC:
            summary[self.kind] = {
                k: sanitize_np_types(v)
                for k, v in self.df.metric.describe().to_dict().items()
            }
            summary[self.kind]["last"] = sanitize_np_types(self.df.metric.iloc[-1])

        return summary


class LoggedEventSpec(namedtuple("LoggedEventSpec", "name kind event")):
    pass


class LoggedEventListSpec(namedtuple("LoggedEventListSpec", "name kind events")):
    def get_csv_header(self) -> str:
        return V1Event.SEPARATOR.join(["step", "timestamp", self.kind])

    def get_csv_events(self) -> str:
        events = ["\n{}".format(e.to_csv()) for e in self.events]
        return "".join(events)

    def empty_events(self):
        self.events[:] = []

    def to_dict(self):
        return {
            "name": self.name,
            "kind": self.kind,
            "events": [e.to_dict() for e in self.events],
        }

    @classmethod
    def from_dict(cls, value: Mapping) -> "LoggedEventListSpec":
        return cls(
            name=value.get("name"),
            kind=value.get("kind"),
            events=[V1Event.from_dict(e) for e in value.get("events", [])],
        )
