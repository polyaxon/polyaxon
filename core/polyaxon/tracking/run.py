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

import atexit
import os
import sys
import time

import polyaxon_sdk

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.client.decorators import (
    can_log_events,
    can_log_outputs,
    check_no_op,
    check_offline,
)
from polyaxon.constants import UNKNOWN
from polyaxon.containers.contexts import (
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
    CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT,
)
from polyaxon.env_vars.getters import (
    get_collect_artifact,
    get_collect_resources,
    get_log_level,
)
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import LoggedEventSpec, V1Event, get_asset_path
from polyaxon.tracking.events import EventFileWriter, events_processors
from polyaxon.tracking.events.writer import ResourceFileWriter
from polyaxon.utils.env import get_run_env
from polyaxon.utils.path_utils import get_path_extension


class Run(RunClient):
    @check_no_op
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        run_uuid: str = None,
        client: RunClient = None,
        track_code: bool = True,
        track_env: bool = False,
        refresh_data: bool = False,
        artifacts_path: str = None,
    ):
        super().__init__(
            owner=owner, project=project, run_uuid=run_uuid, client=client,
        )
        self.track_code = track_code
        self.track_env = track_env
        self._has_model = False
        self._has_dashboard = False
        self._has_tensorboard = False
        self._artifacts_path = None
        self._outputs_path = None
        self._event_logger = None
        self._resource_logger = None
        self._results = {}

        if (settings.CLIENT_CONFIG.is_managed and self.run_uuid) or artifacts_path:
            self.set_artifacts_path(artifacts_path)

        if (
            self.artifacts_path
            and settings.CLIENT_CONFIG.is_managed
            and get_collect_artifact()
        ):
            self.set_run_event_logger()
            if get_collect_resources():
                self.set_run_resource_logger()

        self._run = polyaxon_sdk.V1Run()
        if settings.CLIENT_CONFIG.is_offline:
            return

        if self._run_uuid and (refresh_data or settings.CLIENT_CONFIG.is_managed):
            self.refresh_data()

        # Track run env
        if settings.CLIENT_CONFIG.is_managed and self.track_env:
            self.log_env()

        if settings.CLIENT_CONFIG.is_managed:
            self._register_wait()

    @property
    def is_service(self):
        if settings.CLIENT_CONFIG.no_op:
            return None

        return settings.CLIENT_CONFIG.is_managed and settings.CLIENT_CONFIG.is_service

    @property
    def artifacts_path(self):
        return self._artifacts_path

    @property
    def outputs_path(self):
        return self._outputs_path

    @check_no_op
    @check_offline
    @can_log_outputs
    def get_tensorboard_path(self):
        path = os.path.join(self._outputs_path, "tensorboard")
        if not self._has_tensorboard:
            self.log_tensorboard_ref(path)
            self._has_tensorboard = True
        return path

    @check_no_op
    def set_artifacts_path(self, artifacts_path: str = None):
        _artifacts_path = artifacts_path or CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(
            self.run_uuid
        )
        if artifacts_path:
            _outputs_path = "{}/outputs".format(artifacts_path)
        else:
            _outputs_path = CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format(self.run_uuid)
        self._artifacts_path = _artifacts_path
        self._outputs_path = _outputs_path

    @check_no_op
    def set_run_event_logger(self):
        self._event_logger = EventFileWriter(run_path=self.artifacts_path)

    @check_no_op
    def set_run_resource_logger(self):
        self._resource_logger = ResourceFileWriter(run_path=self.artifacts_path)

    def _post_create(self):
        if self.artifacts_path:
            self.set_run_event_logger()

        if self.track_code:
            self.log_code_ref()
        if self.track_env:
            self.log_env()

        if not settings.CLIENT_CONFIG.is_managed:
            self._start()
        else:
            self._register_wait()

    def _log_dashboard(self):
        if not self._has_dashboard:
            self._has_dashboard = True
            self._log_meta(has_dashboard=True)

    def _log_model(self):
        if not self._has_model:
            self._has_model = True
            self._log_meta(has_model=True)

    @check_no_op
    @check_offline
    @can_log_events
    def log_metric(self, name, value, step=None, timestamp=None):
        self._log_dashboard()

        events = []
        event_value = events_processors.metric(value)
        if event_value == UNKNOWN:
            return
        events.append(
            LoggedEventSpec(
                name=name,
                kind=V1ArtifactKind.METRIC,
                event=V1Event.make(timestamp=timestamp, step=step, metric=event_value),
            )
        )
        if events:
            self._event_logger.add_events(events)
            self._results[name] = event_value

    @check_no_op
    @check_offline
    @can_log_events
    def log_metrics(self, step=None, timestamp=None, **metrics):
        self._log_dashboard()

        events = []
        for metric in metrics:
            event_value = events_processors.metric(metrics[metric])
            if event_value == UNKNOWN:
                continue
            events.append(
                LoggedEventSpec(
                    name=metric,
                    kind=V1ArtifactKind.METRIC,
                    event=V1Event.make(
                        timestamp=timestamp, step=step, metric=event_value
                    ),
                )
            )
        if events:
            self._event_logger.add_events(events)

    @check_no_op
    @check_offline
    @can_log_events
    def log_roc_auc_curve(self, name, fpr, tpr, auc=None, step=None, timestamp=None):
        self._log_dashboard()

        event_value = events_processors.roc_auc_curve(fpr=fpr, tpr=tpr, auc=auc,)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_sklearn_roc_auc_curve(
        self, name, y_preds, y_targets, step=None, timestamp=None
    ):
        self._log_dashboard()

        event_value = events_processors.sklearn_roc_auc_curve(
            y_preds=y_preds, y_targets=y_targets,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_pr_curve(
        self, name, precision, recall, average_precision=None, step=None, timestamp=None
    ):
        self._log_dashboard()

        event_value = events_processors.pr_curve(
            precision=precision, recall=recall, average_precision=average_precision,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_sklearn_pr_curve(self, name, y_preds, y_targets, step=None, timestamp=None):
        self._log_dashboard()

        event_value = events_processors.sklearn_pr_curve(
            y_preds=y_preds, y_targets=y_targets,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_curve(self, name, x, y, annotation=None, step=None, timestamp=None):
        self._log_dashboard()

        event_value = events_processors.curve(x=x, y=y, annotation=annotation,)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_image(
        self, data, name=None, step=None, timestamp=None, rescale=1, dataformats="CHW"
    ):
        self._log_dashboard()

        is_file = isinstance(data, str) and os.path.exists(data)
        ext = "png"
        if is_file:
            name = name or os.path.basename(data)
            ext = get_path_extension(filepath=data) or ext
        else:
            name = name or "image"

        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=V1ArtifactKind.IMAGE,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)
        if is_file:
            event_value = events_processors.image_path(
                from_path=data, asset_path=asset_path
            )
        elif hasattr(data, "encoded_image_string"):
            event_value = events_processors.encoded_image(
                asset_path=asset_path, data=data, asset_rel_path=asset_rel_path,
            )
        else:
            event_value = events_processors.image(
                asset_path=asset_path,
                data=data,
                rescale=rescale,
                dataformats=dataformats,
                asset_rel_path=asset_rel_path,
            )

        if event_value == UNKNOWN:
            return

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.IMAGE,
            event=V1Event.make(timestamp=timestamp, step=step, image=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_image_with_boxes(
        self,
        tensor_image,
        tensor_boxes,
        name=None,
        step=None,
        timestamp=None,
        rescale=1,
        dataformats="CHW",
    ):
        self._log_dashboard()

        name = name or "figure"
        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=V1ArtifactKind.IMAGE,
            name=name,
            step=step,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)
        event_value = events_processors.image_boxes(
            asset_path=asset_path,
            tensor_image=tensor_image,
            tensor_boxes=tensor_boxes,
            rescale=rescale,
            dataformats=dataformats,
            asset_rel_path=asset_rel_path,
        )
        if event_value == UNKNOWN:
            return
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.IMAGE,
            event=V1Event.make(timestamp=timestamp, step=step, image=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_mpl_image(self, data, name=None, close=True, step=None, timestamp=None):
        name = name or "figure"
        if isinstance(data, list):
            event_value = events_processors.figures_to_images(figures=data, close=close)

            if event_value == UNKNOWN:
                return

            self.log_image(
                name=name,
                data=event_value,
                step=step,
                timestamp=timestamp,
                dataformats="NCHW",
            )
        else:
            event_value = events_processors.figure_to_image(figure=data, close=close)
            self.log_image(
                name=name,
                data=event_value,
                step=step,
                timestamp=timestamp,
                dataformats="CHW",
            )

    @check_no_op
    @check_offline
    @can_log_events
    def log_video(
        self, data, name=None, fps=4, step=None, timestamp=None, content_type=None
    ):
        self._log_dashboard()

        is_file = isinstance(data, str) and os.path.exists(data)
        content_type = content_type or "gif"
        if is_file:
            name = name or os.path.basename(data)
            content_type = get_path_extension(filepath=data) or content_type
        else:
            name = name or "video"

        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=V1ArtifactKind.VIDEO,
            name=name,
            step=step,
            ext=content_type,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)
        if is_file:
            event_value = events_processors.video_path(
                from_path=data,
                asset_path=asset_path,
                content_type=content_type,
                asset_rel_path=asset_rel_path,
            )
        else:
            event_value = events_processors.video(
                asset_path=asset_path,
                tensor=data,
                fps=fps,
                content_type=content_type,
                asset_rel_path=asset_rel_path,
            )

        if event_value == UNKNOWN:
            return

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.VIDEO,
            event=V1Event.make(timestamp=timestamp, step=step, video=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_audio(
        self,
        data,
        name=None,
        sample_rate=44100,
        step=None,
        timestamp=None,
        content_type=None,
    ):
        self._log_dashboard()

        is_file = isinstance(data, str) and os.path.exists(data)
        ext = content_type or "wav"
        if is_file:
            name = name or os.path.basename(data)
            ext = get_path_extension(filepath=data) or ext
        else:
            name = name or "audio"

        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=V1ArtifactKind.AUDIO,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)

        if is_file:
            event_value = events_processors.audio_path(
                from_path=data,
                asset_path=asset_path,
                content_type=content_type,
                asset_rel_path=asset_rel_path,
            )
        else:
            event_value = events_processors.audio(
                asset_path=asset_path,
                tensor=data,
                sample_rate=sample_rate,
                asset_rel_path=asset_rel_path,
            )

        if event_value == UNKNOWN:
            return

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.AUDIO,
            event=V1Event.make(timestamp=timestamp, step=step, audio=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_text(self, name, text, step=None, timestamp=None):
        self._log_dashboard()

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.TEXT,
            event=V1Event.make(timestamp=timestamp, step=step, text=text),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_html(self, name, html, step=None, timestamp=None):
        self._log_dashboard()

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.HTML,
            event=V1Event.make(timestamp=timestamp, step=step, html=html),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_np_histogram(self, name, values, counts, step=None, timestamp=None):
        self._log_dashboard()

        event_value = events_processors.np_histogram(values=values, counts=counts)

        if event_value == UNKNOWN:
            return

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.HISTOGRAM,
            event=V1Event.make(timestamp=timestamp, step=step, histogram=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_histogram(
        self, name, values, bins, max_bins=None, step=None, timestamp=None
    ):
        self._log_dashboard()

        event_value = events_processors.histogram(
            values=values, bins=bins, max_bins=max_bins
        )

        if event_value == UNKNOWN:
            return

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.HISTOGRAM,
            event=V1Event.make(timestamp=timestamp, step=step, histogram=event_value),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_model(
        self, path, name=None, framework=None, spec=None, step=None, timestamp=None
    ):
        self._log_model()

        name = name or os.path.basename(path)
        ext = None
        if os.path.isfile(path):
            ext = get_path_extension(filepath=path)

        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=V1ArtifactKind.MODEL,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)
        model = events_processors.model_path(
            from_path=path,
            asset_path=asset_path,
            framework=framework,
            spec=spec,
            asset_rel_path=asset_rel_path,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.MODEL,
            event=V1Event.make(timestamp=timestamp, step=step, model=model),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_dataframe(
        self, path, name=None, content_type=None, step=None, timestamp=None
    ):
        self._log_dashboard()

        name = name or os.path.basename(path)
        ext = get_path_extension(filepath=path)

        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=V1ArtifactKind.DATAFRAME,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)
        df = events_processors.dataframe_path(
            from_path=path,
            asset_path=asset_path,
            content_type=content_type,
            asset_rel_path=asset_rel_path,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.DATAFRAME,
            event=V1Event.make(timestamp=timestamp, step=step, dataframe=df),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_artifact(
        self, path, name=None, artifact_kind=None, step=None, timestamp=None
    ):
        self._log_dashboard()

        name = name or os.path.basename(name)
        ext = get_path_extension(filepath=path)
        artifact_kind = artifact_kind or V1ArtifactKind.FILE

        asset_path = get_asset_path(
            run_path=self.artifacts_path,
            kind=artifact_kind,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self.artifacts_path)

        artifact = events_processors.artifact_path(
            from_path=path,
            asset_path=asset_path,
            kind=artifact_kind,
            asset_rel_path=asset_rel_path,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=artifact_kind,
            event=V1Event.make(timestamp=timestamp, step=step, artifact=artifact),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_plotly_chart(self, name, figure, step=None, timestamp=None):
        self._log_dashboard()

        chart = events_processors.plotly_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_bokeh_chart(self, name, figure, step=None, timestamp=None):
        self._log_dashboard()

        chart = events_processors.bokeh_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    @check_offline
    @can_log_events
    def log_mpl_plotly_chart(self, name, figure, step=None, timestamp=None):
        self._log_dashboard()

        chart = events_processors.mpl_plotly_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._event_logger.add_event(logged_event)

    @check_no_op
    def get_log_level(self):
        return get_log_level()

    @check_no_op
    @check_offline
    def _register_wait(self):
        atexit.register(self._wait)

    @check_no_op
    @check_offline
    def _start(self):
        self.start()
        atexit.register(self._end)

        def excepthook(exception, value, tb):
            self.log_failed(message="Type: {}, Value: {}".format(exception, value))
            # Resume normal work
            sys.__excepthook__(exception, value, tb)

        sys.excepthook = excepthook

    @check_no_op
    @check_offline
    def _end(self):
        self.log_succeeded()
        self._wait()

    @check_no_op
    @check_offline
    def _wait(self):
        if self._event_logger:
            self._event_logger.close()
        if self._resource_logger:
            self._resource_logger.close()
        if self._results:
            self.log_outputs(**self._results)
        time.sleep(settings.CLIENT_CONFIG.tracking_timeout)

    @check_no_op
    @check_offline
    @can_log_outputs
    def log_env(self):
        env_data = get_run_env()
        with open(os.path.join(self.outputs_path, ".polyaxon"), "w") as env_file:
            env_file.write(env_data)
