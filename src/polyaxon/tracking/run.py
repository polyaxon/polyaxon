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

import atexit
import os
import sys
import tempfile
import time

from datetime import datetime
from typing import Dict, List

import polyaxon_sdk
import ujson

from polyaxon import settings
from polyaxon.client import RunClient, get_rel_asset_path
from polyaxon.client.decorators import client_handler
from polyaxon.connections.reader import get_connection_type
from polyaxon.constants.globals import UNKNOWN
from polyaxon.containers import contexts as container_contexts
from polyaxon.containers.contexts import (
    CONTEXTS_EVENTS_SUBPATH_FORMAT,
    CONTEXTS_SYSTEM_RESOURCES_EVENTS_SUBPATH_FORMAT,
)
from polyaxon.env_vars.getters import (
    get_artifacts_store_name,
    get_collect_artifacts,
    get_collect_resources,
    get_log_level,
)
from polyaxon.lifecycle import LifeCycle
from polyaxon.logger import logger
from polyaxon.polyboard.artifacts import V1ArtifactKind, V1RunArtifact
from polyaxon.polyboard.events import LoggedEventSpec, V1Event, get_asset_path
from polyaxon.polyboard.logging import V1Log, V1Logs
from polyaxon.polyboard.processors import events_processors
from polyaxon.polyboard.processors.events_processors import copy_file_or_dir_path
from polyaxon.polyboard.processors.logs_processor import setup_logging
from polyaxon.polyboard.processors.writer import EventFileWriter, ResourceFileWriter
from polyaxon.sidecar.processor import SidecarThread
from polyaxon.utils.env import get_run_env
from polyaxon.utils.fqn_utils import to_fqn_name
from polyaxon.utils.path_utils import (
    check_or_create_path,
    get_base_filename,
    get_path_extension,
)


class Run(RunClient):
    """Run tracking is client to instrument your machine learning model and track experiments.

    If no values are passed to this class,
    Polyaxon will try to resolve the owner, project, and run uuid from the environment:
     * If you have a configured CLI, Polyaxon will use the configuration of the cli.
     * If you have a cached run using the CLI, the client will default to that cached run
       unless you override the values.
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
        owner: str, optional,
             the owner is the username or the organization name owning this project.
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
        collect_artifacts: bool, optional,
             similar to the env var flag `POLYAXON_COLLECT_ARTIFACTS`, this env var is `True`
             by default for managed runs and is controlled by the plugins section.
        collect_resources: bool, optional,
             similar to the env var flag `POLYAXON_COLLECT_RESOURCES`, this env var is `True`
             by default for managed runs and is controlled by the plugins section.
        is_offline: bool, optional,
             To trigger the offline mode manually instead of depending on `POLYAXON_IS_OFFLINE`.
        is_new: bool, optional,
             Force the creation of a new run instead of trying to discover a cached run or
             refreshing an instance from the env var
        name: str, optional,
             When `is_new` or `is_offline` is set to true, a new instance is created and
             you can initialize that new run with a name.
        description: str, optional,
             When `is_new` or `is_offline` is set to true, a new instance is created and
             you can initialize that new run with a description.
        tags: str or List[str], optional,
             When `is_new` or `is_offline` is set to true, a new instance is created and
             you can initialize that new run with tags.

    Raises:
        PolyaxonClientException: If no owner and/or project are passed and Polyaxon cannot
             resolve the values from the environment.
    """

    @client_handler(check_no_op=True)
    def __init__(
        self,
        owner: str = None,
        project: str = None,
        run_uuid: str = None,
        client: RunClient = None,
        track_code: bool = True,
        track_env: bool = True,
        track_logs: bool = True,
        refresh_data: bool = False,
        artifacts_path: str = None,
        collect_artifacts: bool = None,
        collect_resources: bool = None,
        is_offline: bool = None,
        is_new: bool = None,
        name: str = None,
        description: str = None,
        tags: List[str] = None,
        auto_create: bool = True,
    ):
        super().__init__(
            owner=owner,
            project=project,
            run_uuid=run_uuid,
            client=client,
            is_offline=is_offline,
        )
        track_logs = track_logs if track_logs is not None else self._is_offline
        self._logs_history = V1Logs(logs=[])
        self._artifacts_path = None
        self._outputs_path = None
        self._event_logger = None
        self._resource_logger = None
        self._sidecar = None
        self._exit_handler = None

        is_new = is_new or (
            self._run_uuid is None and not settings.CLIENT_CONFIG.is_managed
        )

        if auto_create and (is_new or self._is_offline):
            super().create(name=name, description=description, tags=tags)

        if (
            not is_new
            and self._run_uuid
            and (refresh_data or settings.CLIENT_CONFIG.is_managed)
        ):
            self.refresh_data()

        self._init_artifacts_tracking(
            artifacts_path=artifacts_path,
            collect_artifacts=collect_artifacts,
            collect_resources=collect_resources,
            is_new=is_new,
        )

        # Track run env
        if self._artifacts_path and track_env:
            self.log_env()

        # Track code
        if is_new and track_code:
            self.log_code_ref()

        if is_new and self._artifacts_path and track_logs:
            setup_logging(add_logs=self._add_logs)

        self._set_exit_handler(is_new=is_new)

    def _init_artifacts_tracking(
        self,
        artifacts_path: str = None,
        collect_artifacts: bool = None,
        collect_resources: bool = None,
        is_new: bool = None,
    ):
        if (settings.CLIENT_CONFIG.is_managed and self.run_uuid) or artifacts_path:
            self.set_artifacts_path(artifacts_path, is_related=is_new)
        if not self._artifacts_path and self._is_offline:
            self.set_artifacts_path(artifacts_path)

        # no artifacts path is set, we use the temp path
        if not self._artifacts_path:
            artifacts_path = container_contexts.CONTEXT_ARTIFACTS_FORMAT.format(
                self.run_uuid
            )
            self.set_artifacts_path(artifacts_path)

        if self._artifacts_path and get_collect_artifacts(
            arg=collect_artifacts, default=self._is_offline or is_new
        ):
            self.set_run_event_logger()
            if get_collect_resources(
                arg=collect_resources, default=self._is_offline or is_new
            ):
                self.set_run_resource_logger()
            if not self._is_offline and not settings.CLIENT_CONFIG.is_managed:
                self.set_run_process_sidecar()

    def _add_event(self, event: LoggedEventSpec):
        if self._event_logger:
            self._event_logger.add_event(event)
        else:
            logger.warning(
                "Could not log event {}, "
                "the event logger was not configured properly".format(event.name)
            )

    def _add_events(self, events: List[LoggedEventSpec]):
        if self._event_logger:
            self._event_logger.add_events(events)
        else:
            logger.warning(
                "Could not log events {}, "
                "the event logger was not configured properly".format(len(events))
            )

    def _persist_logs_history(self):
        if self._logs_history.logs and len(self._logs_history.logs) > 0:
            logs_path = os.path.join(
                self._artifacts_path,
                "plxlogs",
                "{}.plx".format(
                    datetime.timestamp(self._logs_history.logs[-1].timestamp)
                ),
            )
            check_or_create_path(logs_path, is_dir=False)
            with open(logs_path, "w") as logs_file:
                logs_file.write(
                    "{}\n{}".format(
                        self._logs_history.get_csv_header(), self._logs_history.to_csv()
                    )
                )

    def _add_logs(self, log: V1Log):
        self._logs_history.logs.append(log)
        if V1Logs.should_chunk(self._logs_history.logs):
            self._persist_logs_history()
            # Reset
            self._logs_history = V1Logs(logs=[])

    def create(self, **kwargs):
        raise NotImplementedError(
            "The tracking `Run` subclass does not allow to call "
            "`create` method manually, please create a new instance of `Run` with `is_new=True`"
        )

    def _get_store_path(self):
        connection = get_connection_type(get_artifacts_store_name())
        if not connection:
            logger.warning("Artifacts store connection not detected.")
        return os.path.join(connection.store_path, self.run_uuid)

    @client_handler(check_no_op=True)
    def get_artifacts_path(
        self,
        rel_path: str = None,
        ensure_path: bool = False,
        is_dir: bool = False,
        use_store_path: bool = False,
    ):
        """Get the absolute path of the specified artifact in the currently active run.

        If `rel_path` is specified, the artifact root path of the currently active
        run will be returned: `root_run_artifacts_path/rel_path`.
        If `rel_path` is not specified, the current root artifacts path configured
        for this instance will be returned: `root_run_artifacts_path`.

        If `ensure_path` is provided, the path will be created. By default the path will
        be created until the last part of the `rel_path` argument,
        if `is_dir` is True, the complete `rel_path` is created.

        If `use_store_path` is enabled, the path returned will be relative to the artifacts
        store path and not Polyaxon's context. Please note that,
        the library will not ensure that the path exists when this flag is set to true.

        Args:
            rel_path: str, optional.
            ensure_path: bool, optional, default True.
            is_dir: bool, optional, default False.
            use_store_path: bool, default False.
        Returns:
            str, artifacts_path
        """
        artifacts_path = (
            self._get_store_path() if use_store_path else self._artifacts_path
        )
        if rel_path:
            path = os.path.join(artifacts_path, rel_path)
            if ensure_path and not use_store_path:
                check_or_create_path(path, is_dir=is_dir)
            return path
        return artifacts_path

    @client_handler(check_no_op=True)
    def get_outputs_path(
        self,
        rel_path: str = None,
        ensure_path: bool = True,
        is_dir: bool = False,
        use_store_path: bool = False,
    ):
        """Get the absolute outputs path of the specified artifact in the currently active run.

        If `rel_path` is specified, the outputs artifact root path of the currently active
        run will be returned: `root_run_artifacts_path/outputs/rel_path`.
        If `rel_path` is not specified, the current root artifacts path configured
        for this instance will be returned: `root_run_artifacts_path/outputs`.

        If `ensure_path` is provided, the path will be created. By default the path will
        be created until the last part of the `rel_path` argument,
        if `is_dir` is True, the complete `rel_path` is created.


        If `use_store_path` is enabled, the path returned will be relative to the artifacts
        store path and not Polyaxon's context. Please note that,
        the library will not ensure that the path exists when this flag is set to true.

        Args:
            rel_path: str, optional.
            ensure_path: bool, optional, default True.
            is_dir: bool, optional, default False.
            use_store_path: bool, default False.
        Returns:
            str, outputs_path
        """
        outputs_path = (
            container_contexts.CONTEXTS_OUTPUTS_SUBPATH_FORMAT.format(
                self._get_store_path()
            )
            if use_store_path
            else self._outputs_path
        )
        if rel_path:
            path = os.path.join(outputs_path, rel_path)
            if ensure_path:
                check_or_create_path(path, is_dir=is_dir)
            return path
        return outputs_path

    @client_handler(check_no_op=True, can_log_outputs=True)
    def get_tensorboard_path(
        self, rel_path: str = "tensorboard", use_store_path: bool = False
    ):
        """Returns a tensorboard path for this run relative to the outputs path.

        If `use_store_path` is enabled, the path returned will be relative to the artifacts
        store path and not Polyaxon's context. Please note that,
        the library will not ensure that the path exists when this flag is set to true.

        Args:
            rel_path: str, optional, default "tensorboard",
                 the relative path to the `outputs` context.
            use_store_path: bool, default False.
        Returns:
            str, outputs_path/rel_path
        """
        path = self.get_outputs_path(rel_path, use_store_path=use_store_path)
        self.log_tensorboard_ref(path)
        return path

    @client_handler(check_no_op=True)
    def set_artifacts_path(self, artifacts_path: str = None, is_related: bool = False):
        """Sets the root artifacts_path.

        > **Note**: Both `in-cluster` and `offline` modes will call this method automatically.
        > Be careful, this method is called automatically. Polyaxon has some processes
        > to automatically sync your run's artifacts and outputs.

        Args:
            artifacts_path: str, optional
            is_related: bool, optional,
                 To create multiple runs in-cluster in a notebook or a vscode session.
        """
        if artifacts_path:
            _artifacts_path = artifacts_path
        elif self._is_offline:
            _artifacts_path = container_contexts.CONTEXT_OFFLINE_FORMAT.format(
                self.run_uuid
            )
        elif is_related:
            _artifacts_path = (
                container_contexts.CONTEXT_MOUNT_ARTIFACTS_RELATED_FORMAT.format(
                    self.run_uuid
                )
            )
        else:
            _artifacts_path = container_contexts.CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(
                self.run_uuid
            )

        _outputs_path = container_contexts.CONTEXTS_OUTPUTS_SUBPATH_FORMAT.format(
            _artifacts_path
        )
        self._artifacts_path = _artifacts_path
        self._outputs_path = _outputs_path

    @client_handler(check_no_op=True)
    def set_run_event_logger(self):
        """Sets an event logger.

        > **Note**: Both `in-cluster` and `offline` modes will call this method automatically.
        > Be careful, this method is called automatically. Polyaxon has some processes
        > to automatically sync your run's artifacts and outputs.
        """
        self._event_logger = EventFileWriter(run_path=self._artifacts_path)

    @client_handler(check_no_op=True)
    def set_run_resource_logger(self):
        """Sets an resources logger.

        > **Note**: Both `in-cluster` and `offline` modes will call this method automatically.
        > Be careful, this method is called automatically. Polyaxon has some processes
        > to automatically sync your run's artifacts and outputs.
        """
        self._resource_logger = ResourceFileWriter(run_path=self._artifacts_path)

    @client_handler(check_no_op=True)
    def set_run_process_sidecar(self):
        """Sets an sidecar process to sync artifacts.

        > **Note**: Both `in-cluster` and `offline` modes will call this method automatically.
        > Be careful, this method is called automatically. Polyaxon has some processes
        > to automatically sync your run's artifacts and outputs.
        """
        self._sidecar = SidecarThread(client=self, run_path=self._artifacts_path)
        self._sidecar.start()

    def _set_exit_handler(self, is_new: bool = False):
        if self._is_offline or is_new:
            self._start()
        elif settings.CLIENT_CONFIG.is_managed:
            self._register_exit_handler(self._wait)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_metric(
        self, name: str, value: float, step: int = None, timestamp: datetime = None
    ):
        """Logs a metric datapoint.

        ```python
        >>> log_metric(name="loss", value=0.01, step=10)
        ```

        > It's very important to log `step` as one of your metrics
        > if you want to compare experiments on the dashboard
        > and use the steps in x-axis instead of timestamps.

        Args:
            name: str, metric name
            value: float, metric value
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
        self._log_has_metrics()

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
            self._add_events(events)
            self._results[name] = event_value

    @client_handler(check_no_op=True, can_log_events=True)
    def log_metrics(self, step: int = None, timestamp: datetime = None, **metrics):
        """Logs multiple metrics.

        ```python
        >>> log_metrics(step=123, loss=0.023, accuracy=0.91)
        ```

        > It's very important to log `step` as one of your metrics
        > if you want to compare experiments on the dashboard
        > and use the steps in x-axis instead of timestamps.

        Args:
            step: int, optional
            timestamp: datetime, optional
            **metrics: **kwargs, key=value
        """
        self._log_has_metrics()

        events = []
        for metric in metrics:
            metric_name = to_fqn_name(metric)
            event_value = events_processors.metric(metrics[metric])
            if event_value == UNKNOWN:
                continue
            events.append(
                LoggedEventSpec(
                    name=metric_name,
                    kind=V1ArtifactKind.METRIC,
                    event=V1Event.make(
                        timestamp=timestamp, step=step, metric=event_value
                    ),
                )
            )
        if events:
            self._add_events(events)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_roc_auc_curve(
        self,
        name: str,
        fpr,
        tpr,
        auc=None,
        step: int = None,
        timestamp: datetime = None,
    ):
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
        name = to_fqn_name(name)
        self._log_has_events()

        event_value = events_processors.roc_auc_curve(
            fpr=fpr,
            tpr=tpr,
            auc=auc,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_sklearn_roc_auc_curve(
        self,
        name: str,
        y_preds,
        y_targets,
        step: int = None,
        timestamp: datetime = None,
        is_multi_class: bool = False,
    ):
        """Calculates and logs ROC/AUC curve using sklearn.

        ```python
        >>> log_sklearn_roc_auc_curve("roc_value", y_preds, y_targets, step=10)
        ```

        If you are logging a multi-class roc curve, you should set
        `is_multi_class=True` to allow persisting curves for all classes.

        Args:
            name: str, name of the curve
            y_preds: List[float] or numpy.array
            y_targets: List[float] or numpy.array
            step: int, optional
            timestamp: datetime, optional
            is_multi_class: bool, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        def create_event(chart_name, y_p, y_t, pos_label=None):
            event_value = events_processors.sklearn_roc_auc_curve(
                y_preds=y_p,
                y_targets=y_t,
                pos_label=pos_label,
            )
            logged_event = LoggedEventSpec(
                name=chart_name,
                kind=V1ArtifactKind.CURVE,
                event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
            )
            self._add_event(logged_event)

        if is_multi_class:
            import numpy as np

            classes = np.unique(y_targets)
            for i in range(len(classes)):
                create_event(
                    "{}_{}".format(name, i), y_preds[:, i], y_targets, classes[i]
                )
        else:
            create_event(name, y_preds, y_targets)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_pr_curve(
        self,
        name: str,
        precision,
        recall,
        average_precision=None,
        step: int = None,
        timestamp: datetime = None,
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
        name = to_fqn_name(name)
        self._log_has_events()

        event_value = events_processors.pr_curve(
            precision=precision,
            recall=recall,
            average_precision=average_precision,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_sklearn_pr_curve(
        self,
        name: str,
        y_preds,
        y_targets,
        step: int = None,
        timestamp: datetime = None,
        is_multi_class: bool = False,
    ):
        """Calculates and logs PR curve using sklearn.

        ```python
        >>> log_sklearn_pr_curve("pr_value", y_preds, y_targets, step=10)
        ```

        If you are logging a multi-class roc curve, you should set
        `is_multi_class=True` to allow persisting curves for all classes.

        Args:
            name: str, name of the event
            y_preds: List[float] or numpy.array
            y_targets: List[float] or numpy.array
            step: int, optional
            timestamp: datetime, optional
            is_multi_class: bool, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        def create_event(chart_name, y_p, y_t, pos_label=None):
            event_value = events_processors.sklearn_pr_curve(
                y_preds=y_p,
                y_targets=y_t,
                pos_label=pos_label,
            )
            logged_event = LoggedEventSpec(
                name=chart_name,
                kind=V1ArtifactKind.CURVE,
                event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
            )
            self._add_event(logged_event)

        if is_multi_class:
            import numpy as np

            classes = np.unique(y_targets)
            for i in range(len(classes)):
                create_event(
                    "{}_{}".format(name, i), y_preds[:, i], y_targets, classes[i]
                )
        else:
            create_event(name, y_preds, y_targets)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_curve(
        self,
        name: str,
        x,
        y,
        annotation=None,
        step: int = None,
        timestamp: datetime = None,
    ):
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
        name = to_fqn_name(name)
        self._log_has_events()

        event_value = events_processors.curve(
            x=x,
            y=y,
            annotation=annotation,
        )
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CURVE,
            event=V1Event.make(timestamp=timestamp, step=step, curve=event_value),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_confusion_matrix(
        self,
        name: str,
        x,
        y,
        z,
        step: int = None,
        timestamp: datetime = None,
    ):
        """Logs a custom curve.

        ```python
        >>> z = [[0.1, 0.3, 0.5, 0.2],
        >>>      [1.0, 0.8, 0.6, 0.1],
        >>>      [0.1, 0.3, 0.6, 0.9],
        >>>      [0.6, 0.4, 0.2, 0.2]]
        >>>
        >>> x = ['healthy', 'multiple diseases', 'rust', 'scab']
        >>> y = ['healthy', 'multiple diseases', 'rust', 'scab']
        >>> log_confusion_matrix("confusion_test", x, y, z, step=11)
        ```

        Args:
            name: str, name of the curve
            x: List[float] or List[str] or numpy.array
            x: List[float] or List[str] or numpy.array
            z: List[List[float]] or List[List[str]] or numpy.array
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        try:
            event_value = events_processors.confusion_matrix(
                x=x,
                y=y,
                z=z,
            )
        except ValueError as e:
            logger.warning(
                "Confusion matrix %s could not be logged, "
                "please make sure you are passing 3 lists/arrays "
                "with the same length. "
                "Error %s",
                name,
                e,
            )
            return
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CONFUSION,
            event=V1Event.make(timestamp=timestamp, step=step, confusion=event_value),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_image(
        self,
        data,
        name: str = None,
        step: int = None,
        timestamp: datetime = None,
        rescale: int = 1,
        dataformats: str = "CHW",
    ):
        """Logs an image.

        ```python
        >>> log_image(data="path/to/image.png", step=10)
        >>> log_image(data=np_array, name="generated_image", step=10)
        ```

        Args:
            data: str or numpy.array, a file path or numpy array
            name: str,
                 name of the image, if a path is passed this can be optional and the name of the file will be used
            step: int, optional
            timestamp: datetime, optional
            rescale: int, optional
            dataformats: str, optional
        """
        self._log_has_events()

        is_file = isinstance(data, str) and os.path.exists(data)
        ext = "png"
        if is_file:
            name = name or get_base_filename(data)
            ext = get_path_extension(filepath=data) or ext
        else:
            name = name or "image"
        name = to_fqn_name(name)

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
                from_path=data,
                asset_path=asset_path,
                asset_rel_path=asset_rel_path,
            )
        elif hasattr(data, "encoded_image_string"):
            event_value = events_processors.encoded_image(
                asset_path=asset_path,
                data=data,
                asset_rel_path=asset_rel_path,
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
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_image_with_boxes(
        self,
        tensor_image,
        tensor_boxes,
        name: str = None,
        step: int = None,
        timestamp: datetime = None,
        rescale: int = 1,
        dataformats: str = "CHW",
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
            tensor_boxes: numpy.array or str:
                 Box data (for detected objects) box should be represented as [x1, y1, x2, y2]
            name: str, name of the image
            step: int, optional
            timestamp: datetime, optional
            rescale: int, optional
            dataformats: str, optional
        """
        self._log_has_events()

        name = name or "figure"
        name = to_fqn_name(name)
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
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_mpl_image(
        self,
        data,
        name: str = None,
        close: bool = True,
        step: int = None,
        timestamp: datetime = None,
    ):
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
        name = to_fqn_name(name)
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

    @client_handler(check_no_op=True, can_log_events=True)
    def log_video(
        self,
        data,
        name: str = None,
        fps: int = 4,
        step: int = None,
        timestamp: datetime = None,
        content_type: int = None,
    ):
        """Logs a video.

        ```python
        >>> log_video("path/to/my_video1"),
        >>> log_video(
        >>>     name="my_vide2",
        >>>     data=np.arange(np.prod((4, 3, 1, 8, 8)), dtype=float).reshape((4, 3, 1, 8, 8))
        >>> )
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
            name = name or get_base_filename(data)
            content_type = get_path_extension(filepath=data) or content_type
        else:
            name = name or "video"
        name = to_fqn_name(name)

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
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_audio(
        self,
        data,
        name: str = None,
        sample_rate: int = 44100,
        step: int = None,
        timestamp: datetime = None,
        content_type: str = None,
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
            name = name or get_base_filename(data)
            ext = get_path_extension(filepath=data) or ext
        else:
            name = name or "audio"
        name = to_fqn_name(name)

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
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_text(
        self, name: str, text: str, step: int = None, timestamp: datetime = None
    ):
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
        name = to_fqn_name(name)
        self._log_has_events()

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.TEXT,
            event=V1Event.make(timestamp=timestamp, step=step, text=text),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_html(
        self, name: str, html: str, step: int = None, timestamp: datetime = None
    ):
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
        name = to_fqn_name(name)
        self._log_has_events()

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.HTML,
            event=V1Event.make(timestamp=timestamp, step=step, html=html),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_np_histogram(
        self, name: str, values, counts, step: int = None, timestamp: datetime = None
    ):
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
        name = to_fqn_name(name)
        self._log_has_events()

        event_value = events_processors.np_histogram(values=values, counts=counts)

        if event_value == UNKNOWN:
            return

        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.HISTOGRAM,
            event=V1Event.make(timestamp=timestamp, step=step, histogram=event_value),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_histogram(
        self,
        name: str,
        values,
        bins,
        max_bins=None,
        step: int = None,
        timestamp: datetime = None,
    ):
        """Logs a histogram.

        ```python
        >>> log_histogram(
        >>>     name="histo",
        >>>     values=np.arange(np.prod((1024,)), dtype=float).reshape((1024,)),
        >>>     bins="auto",
        >>>     step=1
        >>> )
        ```

        Args:
            name: str, name
            values: np.array
            bins: int or str
            max_bins: int, optional
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
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
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_model(
        self,
        path: str,
        name: str = None,
        framework: str = None,
        summary: Dict = None,
        step: int = None,
        timestamp: datetime = None,
        rel_path: str = None,
        versioned: bool = True,
    ):
        """Logs a model or a versioned model if versioned is true or a step value is provided.

        This method will:
         * save the model
         * several versions of the model and create an event file if the step is provided.

        > **Note 1**: This method does a couple things:
        >  * It moves the model under the outputs or the assets directory if the step is provided
        >  * If the step is provided it creates an event file
        >  * It creates a lineage reference to the model or to the event file if the step is provided

        > **Note 2**: If you need to have more control over where the model should be saved and
        > only record a lineage information of that path you can use `log_model_ref`.

        Args:
            path: str, path to the model to log
            name: str, name
            framework: str, optional ,name of the framework
            summary: Dict, optional, key, value information about the model
            step: int, optional
            timestamp: datetime, optional
            rel_path: str, relative path where to store the model
            versioned: bool, to enable the versioned behavior for storing the model
        """
        name = name or get_base_filename(path)
        name = to_fqn_name(name)
        ext = None
        if os.path.isfile(path):
            ext = get_path_extension(filepath=path)

        if versioned or step is not None:
            self._log_has_model()
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
                spec=summary,
                asset_rel_path=asset_rel_path,
            )
            logged_event = LoggedEventSpec(
                name=name,
                kind=V1ArtifactKind.MODEL,
                event=V1Event.make(timestamp=timestamp, step=step, model=model),
            )
            self._add_event(logged_event)
        else:
            asset_path = self.get_outputs_path(rel_path, is_dir=True)
            copy_file_or_dir_path(path, asset_path, True)
            asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
            self.log_model_ref(
                path=asset_path,
                name=name,
                framework=framework,
                summary=summary,
                rel_path=asset_rel_path,
            )

    @client_handler(check_no_op=True, can_log_events=True)
    def log_artifact(
        self,
        path: str,
        name: str = None,
        kind: str = None,
        summary: Dict = None,
        step: int = None,
        timestamp: datetime = None,
        rel_path: str = None,
        versioned: bool = True,
        **kwargs,
    ):
        """Logs a generic artifact or a versioned generic artifact
        if versioned is true or a step value is provided.

        This method will:
         * save the artifact
         * several versions of the artifact and create an event file if the step is provided.

        > **Note 1**: This method does a couple things:
        >  * It moves the artifact under the outputs or the assets directory if the step is provided
        >  * If the step is provided it creates an event file
        >  * It creates a lineage reference to the artifact or to the event file if the step is provided

        > **Note 2**: If you need to have more control over where the artifact should be saved and
        > only record a lineage information of that path you can use `log_artifact_ref`.

        Args:
            path: str, path to the artifact
            name: str, optional, if not provided the name of the file will be used
            kind: optional, str
            summary: Dict, optional,
                 additional summary information to log about data in the lineage table.
            step: int, optional
            timestamp: datetime, optional
            rel_path: str, relative path where to store the artifacts
            versioned: bool, to enable the versioned behavior for storing the artifact
        """
        name = name or get_base_filename(path)
        name = to_fqn_name(name)
        ext = get_path_extension(filepath=path)
        kind = kind or kwargs.get("artifact_kind")  # Backwards compatibility
        kind = kind or V1ArtifactKind.FILE

        if versioned or step is not None:
            self._log_has_events()
            asset_path = get_asset_path(
                run_path=self._artifacts_path,
                kind=kind,
                name=name,
                step=step,
                ext=ext,
            )
            asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)

            artifact = events_processors.artifact_path(
                from_path=path,
                asset_path=asset_path,
                kind=kind,
                asset_rel_path=asset_rel_path,
            )
            logged_event = LoggedEventSpec(
                name=name,
                kind=kind,
                event=V1Event.make(timestamp=timestamp, step=step, artifact=artifact),
            )
            self._add_event(logged_event)
        else:
            asset_path = self.get_outputs_path(rel_path, is_dir=True)
            copy_file_or_dir_path(path, asset_path, True)
            asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
            self.log_artifact_ref(
                path=asset_path,
                name=name,
                kind=kind,
                summary=summary,
                rel_path=asset_rel_path,
            )

    @client_handler(check_no_op=True, can_log_events=True)
    def log_dataframe(
        self,
        df,
        name: str,
        content_type: str = V1ArtifactKind.CSV,
        step: int = None,
        timestamp: datetime = None,
    ):
        """Logs a dataframe.

        Args:
            df: the dataframe to save
            name: str, optional, if not provided the name of the file will be used
            content_type: str, optional, csv or html.
            step: int, optional
            timestamp: datetime, optional
        """
        self._log_has_events()

        name = to_fqn_name(name)
        asset_path = get_asset_path(
            run_path=self._artifacts_path,
            kind=V1ArtifactKind.DATAFRAME,
            name=name,
            step=step,
            ext=content_type,
        )
        asset_rel_path = os.path.relpath(asset_path, self._artifacts_path)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, name)
            path = "{}.{}".format(path, content_type)
            if content_type == V1ArtifactKind.CSV:
                df.to_csv(path)
            elif content_type == V1ArtifactKind.HTML:
                df.to_html(path)
            else:
                raise ValueError(
                    "The content_type `{}` is not supported "
                    "by the method log_dataframe. "
                    "This method supports `csv` or `html`.".format(content_type)
                )
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
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_plotly_chart(
        self, name: str, figure, step: int = None, timestamp: datetime = None
    ):
        """Logs a plotly chart/figure.

        Args:
            name: str, name of the figure
            figure: plotly.figure
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        chart = events_processors.plotly_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_bokeh_chart(
        self, name: str, figure, step: int = None, timestamp: datetime = None
    ):
        """Logs a bokeh chart/figure.

        Args:
            name: str, name of the figure
            figure: bokeh.figure
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        chart = events_processors.bokeh_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_altair_chart(
        self, name: str, figure, step: int = None, timestamp: datetime = None
    ):
        """Logs a vega/altair chart/figure.

        Args:
            name: str, name of the figure
            figure: figure
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        chart = events_processors.altair_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True, can_log_events=True)
    def log_mpl_plotly_chart(
        self, name: str, figure, step: int = None, timestamp: datetime = None
    ):
        """Logs a matplotlib figure to plotly figure.

        Args:
            name: str, name of the figure
            figure: figure
            step: int, optional
            timestamp: datetime, optional
        """
        name = to_fqn_name(name)
        self._log_has_events()

        chart = events_processors.mpl_plotly_chart(figure=figure)
        logged_event = LoggedEventSpec(
            name=name,
            kind=V1ArtifactKind.CHART,
            event=V1Event.make(timestamp=timestamp, step=step, chart=chart),
        )
        self._add_event(logged_event)

    @client_handler(check_no_op=True)
    def get_log_level(self):
        return get_log_level()

    def end(self):
        """Manually end a run and trigger post done logic (artifacts and lineage collection)."""
        if self._exit_handler:
            atexit.unregister(self._exit_handler)
            self._exit_handler()

    def _register_exit_handler(self, func):
        self._exit_handler = func
        atexit.register(self._exit_handler)

    def _start(self, is_new: bool = False):
        if self._is_offline:
            self.load_offline_run(artifacts_path=self._artifacts_path, run_client=self)
            if self.run_data.status:
                logger.info(f"An offline run was found: {self._artifacts_path}")
            else:
                self.log_status(
                    polyaxon_sdk.V1Statuses.CREATED,
                    reason="OfflineOperation",
                    message="Operation is starting",
                )
                logger.info(f"A new offline run started: {self._artifacts_path}")
        if LifeCycle.is_pending(self.status):
            self.start()
        self._register_exit_handler(self._end)

        def excepthook(exception, value, tb):
            self.log_failed(
                reason="ExitHandler",
                message="An exception was raised during the run. "
                "Type: {}, Value: {}".format(exception, value),
            )
            # Resume normal work
            sys.__excepthook__(exception, value, tb)

        sys.excepthook = excepthook

    def _end(self):
        self.log_succeeded()
        self._persist_logs_history()
        self._wait(sync_artifacts=True)
        if self._is_offline:
            self.persist_offline_run(artifacts_path=self._artifacts_path)

    def _wait(self, sync_artifacts: bool = False):
        if self._event_logger:
            self._event_logger.close()
        if self._resource_logger:
            self._resource_logger.close()
        if self._sidecar:
            self._sidecar.close()
        if self._results:
            self.log_outputs(**self._results)
        if sync_artifacts:
            self.sync_events_summaries(
                last_check=None,
                events_path=CONTEXTS_EVENTS_SUBPATH_FORMAT.format(self._artifacts_path),
            )
            self.sync_system_events_summaries(
                last_check=None,
                events_path=CONTEXTS_SYSTEM_RESOURCES_EVENTS_SUBPATH_FORMAT.format(
                    self._artifacts_path
                ),
            )
        time.sleep(settings.CLIENT_CONFIG.tracking_timeout)

    @client_handler(check_no_op=True, can_log_outputs=True)
    def log_env(self, rel_path: str = None, content: Dict = None):
        """Logs information about the environment.

        Called automatically if track_env is set to True.

        Can be called manually, and can accept a custom content as a form of a dictionary.

        Args:
            rel_path: str, optional, default "env.json".
            content: Dict, optional, default to current system information.
        """
        if not os.path.exists(self._outputs_path):
            return
        if not content:
            content = get_run_env()

        rel_path = rel_path or "env.json"
        path = self._outputs_path
        if rel_path:
            path = os.path.join(path, rel_path)

        with open(os.path.join(path), "w") as env_file:
            env_file.write(ujson.dumps(content))

        artifact_run = V1RunArtifact(
            name="env",
            kind=V1ArtifactKind.ENV,
            path=get_rel_asset_path(path=path, is_offline=self._is_offline),
            summary={"path": path},
            is_input=False,
        )
        self.log_artifact_lineage(body=artifact_run)
