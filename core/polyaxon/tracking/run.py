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
import ujson

from polyaxon import settings
from polyaxon.client import RunClient
from polyaxon.client.decorators import (
    can_log_events,
    can_log_outputs,
    check_no_op,
    check_offline,
)
from polyaxon.constants import UNKNOWN
from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS_FORMAT
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

TEMP_RUN_ARTIFACTS = "/tmp/.plxartifacts"


class Run(RunClient):
    """Run tracking is client to instrument your machine learning model and track experiments.

    If no values are passed to this class,
    Polyaxon will try to resolve the owner, project, and run uuid from the environment:
        * If you have a configured CLI, Polyaxon will use the configuration of the cli.
        * If you have a cached run using the CLI,
        the client will default to that cached run unless you override the values.
        * If you use this client in the context of a job or a service managed by Polyaxon,
        a configuration will be available to resolve the values based on that run.

    You can always access the `self.client` to execute more APIs.

    Properties:
        project: str.
        owner: str.
        run_uuid: str.
        run_data: V1Run.
        status: str.
        namespace: str.
        client: [PolyaxonClient](/docs/core/python-library/polyaxon-client/)

    Args:
        owner: str, optional, the owner is the username or
            the organization name owning this project.
        project: str, optional, project name owning the run(s).
        run_uuid: str, optional, run uuid.
        client: [PolyaxonClient](/docs/core/python-library/polyaxon-client/), optional,
            an instance of a configured client, if not passed,
            a new instance will be created based on the available environment.
        track_code: bool, optional, default True, to track code version.
            Polyaxon will try to track information about any repo
            configured in the context where this client is instantiated.
        track_env: bool, optional, default True, to track information about the environment.
        refresh_data: bool, optional, default False, to refresh the run data at instantiation.
        artifacts_path: str, optional, for in-cluster runs it will be set automatically.

    Raises:
        PolyaxonClientException: If no owner and/or project are passed and Polyaxon cannot
            resolve the values from the environment.
    """

    @check_no_op
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        run_uuid: str = None,
        client: RunClient = None,
        track_code: bool = True,
        track_env: bool = True,
        refresh_data: bool = False,
        artifacts_path: str = None,
    ):
        super().__init__(
            owner=owner, project=project, run_uuid=run_uuid, client=client,
        )
        self.track_code = track_code
        self.track_env = track_env
        self._has_model = False
        self._has_events = False
        self._has_tensorboard = False
        self._artifacts_path = None
        self._outputs_path = None
        self._event_logger = None
        self._resource_logger = None
        self._results = {}

        if (settings.CLIENT_CONFIG.is_managed and self.run_uuid) or artifacts_path:
            self.set_artifacts_path(artifacts_path)

        if (
            self._artifacts_path
            and settings.CLIENT_CONFIG.is_managed
            and get_collect_artifact()
        ):
            self.set_run_event_logger()
            if get_collect_resources():
                self.set_run_resource_logger()

        # no artifacts path is set, we use the temp path
        if not self._artifacts_path:
            self._artifacts_path = TEMP_RUN_ARTIFACTS
            self._outputs_path = TEMP_RUN_ARTIFACTS

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

    @check_no_op
    def get_artifacts_path(self):
        """Returns the current artifacts path configured for this instance.
        Returns:
            str, artifacts_path
        """
        return self._artifacts_path

    @check_no_op
    def get_outputs_path(self):
        """Returns the current outputs path configured for this instance.
        Returns:
            str, outputs_path
        """
        return self._outputs_path

    @check_no_op
    def get_model_path(self, rel_path: str = "model"):
        """Returns a model path for this run relative to the outputs path.

        Args:
             rel_path: str, optional, default "model",
                       the relative path to the `outputs` context.
        Returns:
            str, outputs_path / rel_path
        """
        path = self._outputs_path
        if rel_path:
            path = os.path.join(path, rel_path)
        return path

    @check_no_op
    @check_offline
    @can_log_outputs
    def get_tensorboard_path(self, rel_path: str = "tensorboard"):
        """Returns a tensorboard path for this run relative to the outputs path.

        Args:
             rel_path: str, optional, default "tensorboard",
                       the relative path to the `outputs` context.
        Returns:
            str, outputs_path / rel_path
        """
        path = self._outputs_path
        if rel_path:
            path = os.path.join(path, rel_path)
        if not self._has_tensorboard:
            self.log_tensorboard_ref(path)
            self._has_tensorboard = True
        return path

    @check_no_op
    def set_artifacts_path(self, artifacts_path: str = None):
        """Sets an artifacts_path.
        Be careful, this method is called automatically
        when a job is running in-cluster and follows some flags that Polyaxon sets. Polyaxon
        has some processes to automatically sync your run's artifacts and outputs.

        Args:
            artifacts_path: str, optional
        """
        _artifacts_path = artifacts_path or CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(
            self.run_uuid
        )
        _outputs_path = "{}/outputs".format(_artifacts_path)
        self._artifacts_path = _artifacts_path
        self._outputs_path = _outputs_path

    @check_no_op
    def set_run_event_logger(self):
        """Sets an event logger.
        Be careful, this method is called automatically
        when a job is running in-cluster and follows some flags that Polyaxon sets. Polyaxon
        has some processes to automatically sync your run's artifacts and outputs.
        """
        self._event_logger = EventFileWriter(run_path=self._artifacts_path)

    @check_no_op
    def set_run_resource_logger(self):
        """Sets an resources logger.

        Be careful, this method is called automatically
        when a job is running in-cluster and follows some flags that Polyaxon sets. Polyaxon
        has some processes to automatically sync your run's artifacts and outputs.
        """
        self._resource_logger = ResourceFileWriter(run_path=self._artifacts_path)

    def _post_create(self):
        if self._artifacts_path:
            self.set_run_event_logger()

        if self.track_code:
            self.log_code_ref()
        if self.track_env:
            self.log_env()

        if not settings.CLIENT_CONFIG.is_managed:
            self._start()
        else:
            self._register_wait()

    def _log_has_events(self):
        if not self._has_events:
            self._has_events = True
            self._log_meta(has_events=True)

    def _log_has_model(self):
        if not self._has_model:
            self._has_model = True
            self._log_meta(has_model=True)

    @check_no_op
    @check_offline
    @can_log_events
    def log_metric(self, name: str, value: float, step: int = None, timestamp=None):
        """Logs a metric datapoint.

        ```python
        >>> log_metric(name="loss", value=0.01, step=10)
        ```

        > It's very important to log `step` as one of your metrics
        if you want to compare experiments on the dashboard
        and use the steps in x-axis instead of timestamps.

        Args:
            name: str, metric name
            value: float, metric value
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs multiple metrics.

        ```python
        >>> log_metrics(step=123, loss=0.023, accuracy=0.91)
        ```

        > It's very important to log `step` as one of your metrics
        if you want to compare experiments on the dashboard
        and use the steps in x-axis instead of timestamps.

        Args:
            step: int, optional
            timestamp: datetime, optional
            **metrics: **kwargs, key: value
        """
        self._log_has_events()

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
        """Logs ROC/AUC curve. This method expects an already processed values.

        ```python
        >>> log_roc_auc_curve("roc_value", fpr, tpr, auc=0.6, step=1)
        ```
        Args:
            name: str, name of the curve
            fpr: List[float] or numpy.array, false positive rate
            tpr: List[float] or numpy.array, true positive rate
            auc: float, optional, calculated area under curve
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Calculates and logs ROC/AUC curve using sklearn.

        ```python
        >>> log_sklearn_roc_auc_curve("roc_value", y_preds, y_targets, step=10)
        ```

        Args:
            name: str, name of the curve
            y_preds: List[float] or numpy.array
            y_targets: List[float] or numpy.array
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs PR curve. This method expects an already processed values.

        ```python
        >>> log_pr_curve("pr_value", precision, recall, step=10)
        ```

        Args:
            name: str, name of the curve
            y_preds: List[float] or numpy.array
            y_targets: List[float] or numpy.array
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Calculates and logs PR curve using sklearn.

        ```python
        >>> log_sklearn_pr_curve("pr_value", y_preds, y_targets, step=10)
        ```

        Args:
            name: str, name of the event
            y_preds: List[float] or numpy.array
            y_targets: List[float] or numpy.array
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs a custom curve.

        ```python
        >>> log_curve("pr_value", x, y, annotation="more=info", step=10)
        ```

        Args:
            name: str, name of the curve
            x: List[float] or numpy.array
            y: List[float] or numpy.array
            annotation: str, optional
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs an image.

        ```python
        >>> log_image(data="path/to/image.png", step=10)
        >>> log_image(data=np_array, name="generated_image", step=10)
        ```

        Args:
            data: str or numpy.array, a file path or numpy array
            name: str, name of the image,
                  if a path is passed this can be optional and the name of the file will be used
            step: int, optional
            timestamp: datetime, optional
            rescale: int, optional
            dataformats: str, optional
        """
        self._log_has_events()

        is_file = isinstance(data, str) and os.path.exists(data)
        ext = "png"
        if is_file:
            name = name or os.path.basename(data)
            ext = get_path_extension(filepath=data) or ext
        else:
            name = name or "image"

        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.IMAGE,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
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
        """Logs an image with bounding boxes.

        ```python
        >>> log_image_with_boxes(
        >>>     name="my_image",
        >>>     tensor_image=np.arange(np.prod((3, 32, 32)), dtype=float).reshape((3, 32, 32)),
        >>>     tensor_boxes=np.array([[10, 10, 40, 40]]),
        >>> )
        ```

        Args:
            tensor_image: numpy.array or str: Image data or file name
            tensor_boxes: numpy.array or str: Box data (for detected objects)
                        box should be represented as [x1, y1, x2, y2]
            name: str, name of the image
            step: int, optional
            timestamp: datetime, optional
            rescale: int, optional
            dataformats: str, optional
        """
        self._log_has_events()

        name = name or "figure"
        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.IMAGE,
            name=name,
            step=step,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
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
        """Logs a matplotlib image.

        ```python
        >>> log_mpl_image(name="figure", data=figure, step=1, close=False)
        ```

        Args:
            data: matplotlib.pyplot.figure or List[matplotlib.pyplot.figure]
            name: sre, optional, name
            close: bool, optional, default True
            step: int, optional
            timestamp: datetime, optional
        """
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
        """Logs a video.

        ```python
        >>> log_video("path/to/my_video1"),
        >>> log_video(name="my_vide2", data=np.arange(np.prod((4, 3, 1, 8, 8)), dtype=float).reshape((4, 3, 1, 8, 8)))  # noqa
        ```

        Args:
            data: video data or str.
            name: str, optional, if data is a filepath the name will be the name of the file
            fps: int, optional, frames per second
            step: int, optional
            timestamp: datetime, optional
            content_type: str, optional, default "gif"
        """
        self._log_has_events()

        is_file = isinstance(data, str) and os.path.exists(data)
        content_type = content_type or "gif"
        if is_file:
            name = name or os.path.basename(data)
            content_type = get_path_extension(filepath=data) or content_type
        else:
            name = name or "video"

        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.VIDEO,
            name=name,
            step=step,
            ext=content_type,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
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
        """Logs a audio.

        ```python
        >>> log_audio("path/to/my_audio1"),
        >>> log_audio(name="my_audio2", data=np.arange(np.prod((42,)), dtype=float).reshape((42,)))
        ```

        Args:
            data: str or audio data
            name: str, optional, if data is a filepath the name will be the name of the file
            sample_rate: int, optional, sample rate in Hz
            step: int, optional
            timestamp: datetime, optional
            content_type: str, optional, default "wav"
        """
        self._log_has_events()

        is_file = isinstance(data, str) and os.path.exists(data)
        ext = content_type or "wav"
        if is_file:
            name = name or os.path.basename(data)
            ext = get_path_extension(filepath=data) or ext
        else:
            name = name or "audio"

        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.AUDIO,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)

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
        """Logs a text.

        ```python
        >>> log_text(name="text", text="value")
        ```

        Args:
            name: str, name
            text: str, text value
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs an html.

        ```python
        >>> log_html(name="text", html="<p>value</p>")
        ```

        Args:
            name: str, name
            html: str, text value
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs a numpy histogram.

        ```python
        >>> values, counts = np.histogram(np.random.randint(255, size=(1000,)))
        >>> log_np_histogram(name="histo1", values=values, counts=counts, step=1)
        ```

        Args:
            name: str, name
            values: np.array
            counts: np.array
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs a histogram.

        ```python
        >>> log_histogram(name="histo", values=np.arange(np.prod((1024,)), dtype=float).reshape((1024,)), bins="auto", step=1)  # noqa
        ```

        Args:
            name: str, name
            values: np.array
            bins: int or str
            max_bins: int, optional
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs a model.

        Args:
            path: str, path to the model to log
            name: str, name
            framework: str, optional ,name of the framework
            spec: Dict, optional, key, value information about the model
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_model()

        name = name or os.path.basename(path)
        ext = None
        if os.path.isfile(path):
            ext = get_path_extension(filepath=path)

        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.MODEL,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
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
        """Logs a dataframe.

        Args:
            path: path to the dataframe saved as file
            name: str, optional, if not provided the name of the file will be used
            content_type: str, optional
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

        name = name or os.path.basename(path)
        ext = get_path_extension(filepath=path)

        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.DATAFRAME,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
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
        """Logs a generic artifact.

        Args:
            path: str, path to the artifact
            name: str, optional, if not provided the name of the file will be used
            artifact_kind: optional, str
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

        name = name or os.path.basename(name)
        ext = get_path_extension(filepath=path)
        artifact_kind = artifact_kind or V1ArtifactKind.FILE

        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=artifact_kind,
            name=name,
            step=step,
            ext=ext,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)

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
        """Logs a plotly chart/figure.

        Args:
            name: str, name of the figure
            figure: plotly.figure
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs a bokeh chart/figure.

        Args:
            name: str, name of the figure
            figure: bokeh.figure
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
    def log_altair_chart(self, name, figure, step=None, timestamp=None):
        """Logs a vega/altair chart/figure.

        Args:
            name: str, name of the figure
            figure: figure
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

        chart = events_processors.altair_chart(figure=figure)
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
        """Logs a matplotlib figure to plotly figure.

        Args:
            name: str, name of the figure
            figure: figure
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

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
        """Logs information about the environment.

        Called automatically if track_env is set to True.
        """
        env_data = get_run_env()
        with open(os.path.join(self._outputs_path, "env.json"), "w") as env_file:
            env_file.write(ujson.dumps(env_data))
