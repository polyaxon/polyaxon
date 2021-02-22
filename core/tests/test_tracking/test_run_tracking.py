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

import numpy as np
import os
import pandas as pd
import pytest
import tempfile
import uuid

from unittest.mock import patch

import altair as alt
import matplotlib.pyplot as plt

from bokeh.plotting import figure
from plotly import figure_factory

from polyaxon import settings
from polyaxon.constants import DEFAULT, PLATFORM_DIST_CE
from polyaxon.containers.contexts import (
    CONTEXT_ARTIFACTS_FORMAT,
    CONTEXT_MOUNT_ARTIFACTS_FORMAT,
    CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT,
    CONTEXT_OFFLINE_FORMAT,
    CONTEXTS_OUTPUTS_SUBPATH_FORMAT,
)
from polyaxon.env_vars import getters
from polyaxon.env_vars.getters import get_run_info
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_COLLECT_ARTIFACTS,
    POLYAXON_KEYS_COLLECT_RESOURCES,
    POLYAXON_KEYS_LOG_LEVEL,
    POLYAXON_KEYS_RUN_INSTANCE,
)
from polyaxon.exceptions import PolyaxonClientException
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyboard.events import V1Events, get_asset_path, get_event_path
from polyaxon.polyboard.processors.writer import EventFileWriter, ResourceFileWriter
from polyaxon.tracking.run import Run
from polyaxon.utils.path_utils import create_path
from tests.utils import TestEnvVarsCase, tensor_np


@pytest.mark.tracking_mark
class TestRunTracking(TestEnvVarsCase):
    def setUp(self):
        super().setUp()
        settings.CLIENT_CONFIG.is_managed = True
        settings.CLIENT_CONFIG.is_offline = True

    def test_get_collect_artifacts_return_false_out_cluster(self):
        settings.CLIENT_CONFIG.is_managed = False
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "false"
        assert getters.get_collect_artifacts() is False

    def test_empty_collect_artifacts_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        assert getters.get_collect_artifacts() is False

    def test_valid_artifacts_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_valid_value(
            POLYAXON_KEYS_COLLECT_ARTIFACTS, getters.get_collect_artifacts, "true", True
        )

    def test_get_collect_resources_return_false_out_cluster(self):
        settings.CLIENT_CONFIG.is_managed = False
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "false"
        assert getters.get_collect_resources() is False

    def test_empty_collect_resources_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        assert getters.get_collect_resources() is False

    def test_valid_resources_path(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_valid_value(
            POLYAXON_KEYS_COLLECT_RESOURCES, getters.get_collect_resources, "true", True
        )

    def test_get_log_level_out_cluster(self):
        settings.CLIENT_CONFIG.is_managed = False
        self.check_empty_value(POLYAXON_KEYS_LOG_LEVEL, getters.get_log_level)

    def test_empty_log_level(self):
        settings.CLIENT_CONFIG.is_managed = True
        self.check_empty_value(POLYAXON_KEYS_LOG_LEVEL, getters.get_log_level)

    def test_run_info_checks_is_managed(self):
        settings.CLIENT_CONFIG.is_managed = False
        with self.assertRaises(PolyaxonClientException):
            get_run_info()

    def test_empty_run_info(self):
        self.check_raise_for_invalid_value(
            POLYAXON_KEYS_RUN_INSTANCE, get_run_info, None, PolyaxonClientException
        )

    def test_non_valid_run_info(self):
        self.check_raise_for_invalid_value(
            POLYAXON_KEYS_RUN_INSTANCE,
            get_run_info,
            "something random",
            PolyaxonClientException,
        )

        self.check_raise_for_invalid_value(
            POLYAXON_KEYS_RUN_INSTANCE,
            get_run_info,
            "foo.bar",
            PolyaxonClientException,
        )

    def test_dict_run_info(self):
        uid = uuid.uuid4().hex
        run_info = "user.project_bar.runs.{}".format(uid)
        self.check_valid_value(
            POLYAXON_KEYS_RUN_INSTANCE,
            get_run_info,
            run_info,
            ("user", "project_bar", uid),
        )

    @patch("polyaxon.managers.base.os.path.expanduser")
    def test_run_init(self, expanduser):
        expanduser.return_value = tempfile.mkdtemp()
        settings.CLIENT_CONFIG.is_managed = False
        settings.CLIENT_CONFIG.is_offline = False
        with self.assertRaises(PolyaxonClientException):
            Run()

        # Uses default as owner in non CE
        with self.assertRaises(PolyaxonClientException):
            Run(project="test")

        # Uses default as owner in CE
        settings.CLIENT_CONFIG.is_offline = True
        settings.CLI_CONFIG.installation = {"dist": PLATFORM_DIST_CE}
        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            run = Run(project="test", track_code=False, track_env=False)
        assert exit_mock.call_count == 1
        assert run.owner == DEFAULT

        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            run = Run(
                owner="owner-test", project="test", track_code=False, track_env=False
            )
        assert exit_mock.call_count == 1
        assert run.owner == "owner-test"
        assert run.project == "test"

        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            run = Run(project="owner-test.test")
        assert exit_mock.call_count == 1
        assert run.owner == "owner-test"
        assert run.project == "test"

        settings.CLIENT_CONFIG.is_managed = True
        settings.CLIENT_CONFIG.is_offline = False
        with self.assertRaises(PolyaxonClientException):
            Run()

        settings.CLI_CONFIG.installation = None
        # Uses default as owner in non CE
        with self.assertRaises(PolyaxonClientException):
            Run(project="test")

        # Uses default as owner in CE
        settings.CLIENT_CONFIG.is_offline = True
        settings.CLI_CONFIG.installation = {"dist": PLATFORM_DIST_CE}
        run = Run(project="test")
        assert run.owner == DEFAULT

        # FQN non CE
        settings.CLI_CONFIG.installation = None
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "user.project_bar.runs.uid"
        run = Run()
        assert run.owner == "user"
        assert run.project == "project_bar"
        assert run.run_uuid == "uid"

        # FQN CE
        settings.CLI_CONFIG.installation = {"dist": PLATFORM_DIST_CE}
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "user.project_bar.runs.uid"
        run = Run()
        assert run.owner == "user"
        assert run.project == "project_bar"
        assert run.run_uuid == "uid"

    def test_event_logger_from_non_managed_run(self):
        settings.CLIENT_CONFIG.is_managed = False
        settings.CLIENT_CONFIG.is_offline = False

        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            run = Run(
                project="owner-test.test",
                track_code=False,
                track_env=False,
                collect_artifacts=False,
            )
        assert exit_mock.call_count == 1
        artifacts_context = CONTEXT_ARTIFACTS_FORMAT.format(run.run_uuid)
        assert run.get_artifacts_path() == artifacts_context
        assert run.get_outputs_path() == CONTEXTS_OUTPUTS_SUBPATH_FORMAT.format(
            artifacts_context
        )
        assert run._event_logger is None

        # Add run id
        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            run = Run(
                project="owner-test.test",
                run_uuid="uuid",
                track_code=False,
                track_env=False,
                collect_artifacts=False,
            )
        assert exit_mock.call_count == 1
        artifacts_context = CONTEXT_ARTIFACTS_FORMAT.format(run.run_uuid)
        assert run.get_artifacts_path() == artifacts_context
        assert run.get_outputs_path() == CONTEXTS_OUTPUTS_SUBPATH_FORMAT.format(
            artifacts_context
        )
        assert run._event_logger is None

        run.set_artifacts_path()
        assert run.get_artifacts_path() == CONTEXT_MOUNT_ARTIFACTS_FORMAT.format("uuid")
        assert run.get_outputs_path() == CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("uuid")

        with patch("polyaxon.tracking.run.EventFileWriter") as mock_call:
            run.set_run_event_logger()
        assert mock_call.call_count == 1

        with patch("polyaxon.tracking.run.ResourceFileWriter") as mock_call:
            run.set_run_resource_logger()
        assert mock_call.call_count == 1

        # Set collect flag
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "true"
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "true"
        settings.CLIENT_CONFIG.is_managed = True
        with patch("polyaxon.tracking.run.EventFileWriter") as event_call:
            with patch("polyaxon.tracking.run.ResourceFileWriter") as resource_call:
                with patch("polyaxon.tracking.run.Run.refresh_data") as refresh_call:
                    run = Run(project="owner-test.test", run_uuid="uuid")

        assert refresh_call.call_count == 1
        assert event_call.call_count == 1
        assert resource_call.call_count == 1
        assert run.get_artifacts_path() == CONTEXT_MOUNT_ARTIFACTS_FORMAT.format("uuid")
        assert run.get_outputs_path() == CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("uuid")

    def test_event_logger_from_a_managed_run(self):
        # Set managed flag
        settings.CLIENT_CONFIG.is_managed = True
        settings.CLIENT_CONFIG.is_offline = False
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "user.project_bar.runs.uid"
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "false"
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "false"

        with patch("polyaxon.tracking.run.Run.refresh_data") as refresh_call:
            run = Run()
        assert refresh_call.call_count == 1
        assert run.get_artifacts_path() == CONTEXT_MOUNT_ARTIFACTS_FORMAT.format("uid")
        assert run.get_outputs_path() == CONTEXT_MOUNT_RUN_OUTPUTS_FORMAT.format("uid")
        assert run._event_logger is None

        # Set collect flag
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "true"
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "true"

        # Add run id
        with patch("polyaxon.tracking.run.Run.set_run_event_logger") as event_call:
            with patch(
                "polyaxon.tracking.run.Run.set_run_resource_logger"
            ) as resource_call:
                with patch("polyaxon.tracking.run.Run.refresh_data") as refresh_call:
                    Run(project="test.test", run_uuid="uuid")
        assert event_call.call_count == 1
        assert resource_call.call_count == 1
        assert refresh_call.call_count == 1

        # Set run info
        os.environ[POLYAXON_KEYS_RUN_INSTANCE] = "user.project_bar.runs.uid"
        # Add run id
        with patch("polyaxon.tracking.run.Run.set_run_event_logger") as event_call:
            with patch(
                "polyaxon.tracking.run.Run.set_run_resource_logger"
            ) as resource_call:
                with patch("polyaxon.tracking.run.Run.refresh_data") as refresh_call:
                    Run()
        assert event_call.call_count == 1
        assert resource_call.call_count == 1
        assert refresh_call.call_count == 1

    def test_event_logger_from_an_offline_run(self):
        # Set managed flag
        settings.CLIENT_CONFIG.is_managed = False
        settings.CLIENT_CONFIG.is_offline = True
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "false"
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "false"

        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            run = Run(project="test.test", run_uuid="uid")
        assert exit_mock.call_count == 1
        artifacts_path = CONTEXT_OFFLINE_FORMAT.format("uid")
        assert run.get_artifacts_path() == artifacts_path
        assert run.get_outputs_path() == CONTEXTS_OUTPUTS_SUBPATH_FORMAT.format(
            artifacts_path
        )
        assert run._event_logger is None

        # Set collect flag
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "true"
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "true"

        # Add run id
        with patch("polyaxon.tracking.run.Run.set_run_event_logger") as event_call:
            with patch(
                "polyaxon.tracking.run.Run.set_run_resource_logger"
            ) as resource_call:
                with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
                    Run(project="test.test", run_uuid="uid")
        assert exit_mock.call_count == 1
        assert event_call.call_count == 1
        assert resource_call.call_count == 1


@pytest.mark.tracking_mark
class TestRunLogging(TestEnvVarsCase):
    def setUp(self):
        super().setUp()
        self.run_path = tempfile.mkdtemp()
        settings.CLIENT_CONFIG.is_managed = False
        os.environ[POLYAXON_KEYS_COLLECT_ARTIFACTS] = "false"
        os.environ[POLYAXON_KEYS_COLLECT_RESOURCES] = "false"
        with patch("polyaxon.tracking.run.Run._set_exit_handler") as exit_mock:
            self.run = Run(project="owner.project", track_env=False, track_code=False)
        assert exit_mock.call_count == 1
        self.event_logger = EventFileWriter(run_path=self.run_path)
        self.resource_logger = ResourceFileWriter(run_path=self.run_path)
        self.run._artifacts_path = self.run_path
        self.run._event_logger = self.event_logger
        self.run._resource_logger = self.resource_logger
        assert os.path.exists(get_event_path(self.run_path)) is True
        assert os.path.exists(get_asset_path(self.run_path)) is True

    @staticmethod
    def touch(path):
        with open(path, "w") as f:
            f.write("test")

    def test_log_empty_metric(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_metrics") as log_metrics:
            self.run.log_metrics()
        assert log_metrics.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )

    def test_log_single_metric(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_metrics") as log_metrics:
            self.run.log_metrics(step=1, metric1=1.1)
        assert log_metrics.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.METRIC, name="metric1"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="metric", name="metric1", data=events_file)
        assert len(results.df.values) == 1

    def test_log_multiple_metrics(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_metrics") as log_metrics:
            self.run.log_metrics(step=1, metric1=1.1, metric2=21.1)
        assert log_metrics.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.METRIC, name="metric1"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="metric", name="metric1", data=events_file)
        assert len(results.df.values) == 1

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.METRIC, name="metric2"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="metric", name="metric2", data=events_file)
        assert len(results.df.values) == 1

        with patch("polyaxon.tracking.run.Run._log_has_metrics") as log_metrics:
            self.run.log_metrics(step=2, metric1=1.1, metric2=21.1, metric3=12.1)
        assert log_metrics.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.METRIC))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.METRIC, name="metric1"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="metric", name="metric1", data=events_file)
        assert len(results.df.values) == 2
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.METRIC, name="metric2"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="metric", name="metric2", data=events_file)
        assert len(results.df.values) == 2
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.METRIC, name="metric3"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="metric", name="metric3", data=events_file)
        assert len(results.df.values) == 1

    def test_log_image_from_path(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        image_file = tempfile.mkdtemp() + "/file.png"
        self.touch(image_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_image:
            self.run.log_image(name="my_image", data=image_file)
        assert log_image.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="my_image", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image", ext="png"
        )
        assert os.path.exists(asset_file) is True

    def test_log_image_from_path_with_step(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        image_file = tempfile.mkdtemp() + "/file.png"
        self.touch(image_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_image:
            self.run.log_image(name="my_image", data=image_file, step=1)
        assert log_image.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="my_image", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image", step=1, ext="png"
        )
        assert os.path.exists(asset_file) is True

    def test_log_data_image(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_image:
            self.run.log_image(
                name="my_image", data=tensor_np(shape=(1, 8, 8)), dataformats="CHW"
            )
        assert log_image.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="my_image", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image", ext="png"
        )
        assert os.path.exists(asset_file) is True

    def test_log_image_with_boxes(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        image_file = tempfile.mkdtemp() + "/file.png"
        self.touch(image_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_image_with_boxes:
            self.run.log_image_with_boxes(
                name="my_image",
                tensor_image=tensor_np(shape=(3, 32, 32)),
                tensor_boxes=np.array([[10, 10, 40, 40]]),
            )
        assert log_image_with_boxes.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="my_image", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="my_image"
        )
        assert os.path.exists(asset_file) is True

    def test_log_mpl_image(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )

        figure, axes = plt.figure(), plt.gca()
        circle1 = plt.Circle((0.2, 0.5), 0.2, color="r")
        circle2 = plt.Circle((0.8, 0.5), 0.2, color="g")
        axes.add_patch(circle1)
        axes.add_patch(circle2)
        plt.axis("scaled")
        plt.tight_layout()

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_mpl_image:
            self.run.log_mpl_image(name="figure", data=figure, step=1, close=False)
        assert log_mpl_image.call_count == 1
        assert plt.fignum_exists(figure.number) is True

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="figure", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure", step=1, ext="png"
        )
        assert os.path.exists(asset_file) is True

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_dashboard:
            self.run.log_mpl_image(name="figure", data=figure, step=2)
        assert log_dashboard.call_count == 1
        assert plt.fignum_exists(figure.number) is False

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="figure", data=events_file)
        assert len(results.df.values) == 2

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure", step=1, ext="png"
        )
        assert os.path.exists(asset_file) is True

    @pytest.mark.filterwarnings("ignore::FutureWarning")
    def test_log_mpl_images(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is False
        )

        figures = []
        for i in range(5):
            figure = plt.figure()
            plt.plot([i * 1, i * 2, i * 3], label="Plot " + str(i))
            plt.xlabel("X")
            plt.xlabel("Y")
            plt.legend()
            plt.tight_layout()
            figures.append(figure)

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_mpl_image:
            self.run.log_mpl_image(name="figure", data=figures, step=1, close=False)
        assert log_mpl_image.call_count == 1
        assert all([plt.fignum_exists(figure.number) is True for figure in figures])

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="figure", data=events_file)
        assert len(results.df.values) == 1

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_mpl_image:
            self.run.log_mpl_image(name="figure", data=figures, step=2)
        assert log_mpl_image.call_count == 1
        assert all([plt.fignum_exists(figure.number) is False for figure in figures])

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.IMAGE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="figure", data=events_file)
        assert len(results.df.values) == 2

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.IMAGE, name="figure", step=1, ext="png"
        )
        assert os.path.exists(asset_file) is True

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_log_mpl_plotly(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )

        figure, axes = plt.figure(), plt.gca()
        circle1 = plt.Circle((0.2, 0.5), 0.2, color="r")
        circle2 = plt.Circle((0.8, 0.5), 0.2, color="g")
        axes.add_patch(circle1)
        axes.add_patch(circle2)
        plt.axis("scaled")
        plt.tight_layout()

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_mpl_plotly_chart:
            self.run.log_mpl_plotly_chart(name="figure", figure=figure, step=1)
        assert log_mpl_plotly_chart.call_count == 1

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.CHART))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CHART, name="figure"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="figure", data=events_file)
        assert len(results.df.values) == 1

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_mpl_plotly_chart:
            self.run.log_mpl_plotly_chart(name="figure", figure=figure, step=2)
        assert log_mpl_plotly_chart.call_count == 1
        assert plt.fignum_exists(figure.number) is False

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.CHART))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CHART, name="figure"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="image", name="figure", data=events_file)
        assert len(results.df.values) == 2

    def test_log_video_from_path(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is False
        )
        video_file = tempfile.mkdtemp() + "/video.gif"
        self.touch(video_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_video:
            self.run.log_video(name="my_video", data=video_file)
        assert log_video.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.VIDEO, name="my_video"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="video", name="my_video", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.VIDEO, name="my_video", ext="gif"
        )
        assert os.path.exists(asset_file) is True

    def test_log_data_video(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_dashboard:
            self.run.log_video(name="my_video", data=tensor_np(shape=(4, 3, 1, 8, 8)))
        assert log_dashboard.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.VIDEO))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.VIDEO, name="my_video"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="video", name="my_video", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.VIDEO, name="my_video", ext="gif"
        )
        assert os.path.exists(asset_file) is True

    def test_log_audio_from_path(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is False
        )
        audio_file = tempfile.mkdtemp() + "/audio.wav"
        self.touch(audio_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_audio:
            self.run.log_audio(name="my_audio", data=audio_file)
        assert log_audio.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.AUDIO, name="my_audio"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="audio", name="my_audio", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.AUDIO, name="my_audio", ext="wav"
        )
        assert os.path.exists(asset_file) is True

    def test_log_data_audio(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_audio:
            self.run.log_audio(name="my_audio", data=tensor_np(shape=(42,)))
        assert log_audio.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.AUDIO))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.AUDIO, name="my_audio"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="audio", name="my_audio", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.AUDIO, name="my_audio", ext="wav"
        )
        assert os.path.exists(asset_file) is True

    def test_log_text(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TEXT))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TEXT))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_text:
            self.run.log_text(name="my_text", text="some text", step=1)
        assert log_text.call_count == 1

        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TEXT))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TEXT))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.TEXT, name="my_text"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="text", name="my_text", data=events_file)
        assert len(results.df.values) == 1

    def test_log_html(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.HTML))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.HTML))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_html:
            self.run.log_html(name="my_div", html="<div>test<div/>", step=1)
        assert log_html.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.HTML))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.HTML))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.HTML, name="my_div"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="html", name="my_div", data=events_file)
        assert len(results.df.values) == 1

    def test_log_histogram(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_histogram:
            self.run.log_histogram(
                name="histo", values=tensor_np(shape=(1024,)), bins="auto", step=1
            )
            self.run.log_histogram(
                name="histo", values=tensor_np(shape=(1024,)), bins="fd", step=1
            )
            self.run.log_histogram(
                name="histo", values=tensor_np(shape=(1024,)), bins="doane", step=1
            )
        assert log_histogram.call_count == 3
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.HISTOGRAM, name="histo"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="histogram", name="histo", data=events_file)
        assert len(results.df.values) == 3

    def test_log_np_histogram(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is False
        )
        values, counts = np.histogram(np.random.randint(255, size=(1000,)))
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_np_histogram:
            self.run.log_np_histogram(
                name="histo", values=values, counts=counts, step=1
            )
        assert log_np_histogram.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.HISTOGRAM))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.HISTOGRAM, name="histo"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="histogram", name="histo", data=events_file)
        assert len(results.df.values) == 1

    def test_log_model_file(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is False
        )
        model_file = tempfile.mkdtemp() + "model.pkl"
        self.touch(model_file)
        with patch("polyaxon.tracking.run.Run._log_has_model") as log_model:
            self.run.log_model(name="my_model", path=model_file, framework="scikit")
        assert log_model.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.MODEL, name="my_model"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="model", name="my_model", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.MODEL, name="my_model", ext="pkl"
        )
        assert os.path.exists(asset_file) is True

    def test_log_model_dir(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is False
        )
        model_dir = tempfile.mkdtemp() + "/model"
        create_path(model_dir)
        model_file = model_dir + "/model.pkl"
        self.touch(model_file)
        weights_file = model_dir + "/weights"
        self.touch(weights_file)
        configs_file = model_dir + "/configs"
        self.touch(configs_file)
        with patch("polyaxon.tracking.run.Run._log_has_model") as log_model:
            self.run.log_model(name="my_model", path=model_dir, framework="tensorflow")
        assert log_model.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.MODEL))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.MODEL, name="my_model"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="model", name="my_model", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.MODEL, name="my_model"
        )
        assert os.path.exists(asset_file) is True

    def test_log_dataframe(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is False
        )
        model_file = tempfile.mkdtemp() + "/df.pkl"
        self.touch(model_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_dataframe:
            self.run.log_dataframe(
                name="dataframe", path=model_file, content_type="pickel"
            )
        assert log_dataframe.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.DATAFRAME, name="dataframe"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind="dataframe", name="dataframe", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.DATAFRAME, name="dataframe", ext="pkl"
        )
        assert os.path.exists(asset_file) is True

    def test_log_artifact(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TSV))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TSV))
            is False
        )
        tsv_file = tempfile.mkdtemp() + "/file.tsv"
        self.touch(tsv_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_artifact:
            self.run.log_artifact(
                name="file", path=tsv_file, artifact_kind=V1ArtifactKind.TSV
            )
        assert log_artifact.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TSV))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TSV))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.TSV, name="file"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind=V1ArtifactKind.TSV, name="file", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.TSV, name="file", ext="tsv"
        )
        assert os.path.exists(asset_file) is True

    def test_log_artifact_without_name(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TSV))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TSV))
            is False
        )
        tsv_file = tempfile.mkdtemp() + "/file.tsv"
        self.touch(tsv_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_artifact:
            self.run.log_artifact(path=tsv_file, artifact_kind=V1ArtifactKind.TSV)
        assert log_artifact.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TSV))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TSV))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.TSV, name="file"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind=V1ArtifactKind.TSV, name="file", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.TSV, name="file", ext="tsv"
        )
        assert os.path.exists(asset_file) is True

    def test_log_artifact_without_name_and_filename_with_several_dots(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.FILE))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.FILE))
            is False
        )
        tar_file = tempfile.mkdtemp() + "/file.tar.gz"
        self.touch(tar_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_artifact:
            self.run.log_artifact(path=tar_file, artifact_kind=V1ArtifactKind.FILE)
        assert log_artifact.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.FILE))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.FILE))
            is True
        )
        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.FILE, name="file"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind=V1ArtifactKind.FILE, name="file", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.FILE, name="file", ext="tar.gz"
        )
        assert os.path.exists(asset_file) is True

    def test_log_artifacts(self):
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TSV))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TSV))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is False
        )
        tsv_file = tempfile.mkdtemp() + "/file.tsv"
        self.touch(tsv_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_artifact:
            self.run.log_artifact(
                name="file", path=tsv_file, artifact_kind=V1ArtifactKind.TSV
            )
        assert log_artifact.call_count == 1
        pd_file = tempfile.mkdtemp() + "/dataframe"
        self.touch(pd_file)
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_artifact:
            self.run.log_artifact(
                name="file2", path=pd_file, artifact_kind=V1ArtifactKind.DATAFRAME
            )
        assert log_artifact.call_count == 1
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.TSV))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.TSV))
            is True
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is True
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.DATAFRAME))
            is True
        )

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.TSV, name="file"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind=V1ArtifactKind.TSV, name="file", data=events_file)
        assert len(results.df.values) == 1

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.DATAFRAME, name="file2"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(kind=V1ArtifactKind.TSV, name="file", data=events_file)
        assert len(results.df.values) == 1

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.TSV, name="file", ext="tsv"
        )
        assert os.path.exists(asset_file) is True

        asset_file = get_asset_path(
            self.run_path, kind=V1ArtifactKind.DATAFRAME, name="file2"
        )
        assert os.path.exists(asset_file) is True

    def test_log_charts(self):
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]
        bokeh_test = figure(
            title="simple line example", x_axis_label="x", y_axis_label="y"
        )
        bokeh_test.line(x, y, line_width=2)

        x1 = np.random.randn(200) - 2
        x2 = np.random.randn(200)
        x3 = np.random.randn(200) + 2
        hist_data = [x1, x2, x3]
        group_labels = ["Group 1", "Group 2", "Group 3"]
        plotly_test = figure_factory.create_distplot(
            hist_data, group_labels, bin_size=[0.1, 0.25, 0.5]
        )

        df1 = pd.DataFrame([["A", "B", "C", "D"], [28, 55, 43, 91]], index=["a", "b"]).T
        alt_test = alt.Chart(df1).mark_bar().encode(x="a", y="b")

        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )
        with patch("polyaxon.tracking.run.Run._log_has_events") as log_charts:
            self.run.log_bokeh_chart(name="bokeh_test", figure=bokeh_test, step=1)
            self.run.log_plotly_chart(name="plotly_test", figure=plotly_test, step=1)
            self.run.log_altair_chart(name="alt_test", figure=alt_test, step=1)
        assert log_charts.call_count == 3
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.CHART))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.CHART))
            is True
        )

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CHART, name="bokeh_test"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(
            kind=V1ArtifactKind.CHART, name="bokeh_test", data=events_file
        )
        assert len(results.df.values) == 1

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CHART, name="plotly_test"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(
            kind=V1ArtifactKind.CHART, name="plotly_test", data=events_file
        )
        assert len(results.df.values) == 1

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CHART, name="alt_test"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(
            kind=V1ArtifactKind.CHART, name="alt_test", data=events_file
        )
        assert len(results.df.values) == 1

    def test_log_curves(self):
        x = [1, 2, 3, 4, 5]
        y = [6, 7, 2, 4, 5]

        with patch("polyaxon.tracking.run.Run._log_has_events") as log_curves:
            self.run.log_roc_auc_curve(name="roc_test", fpr=x, tpr=y, auc=0.6, step=1)
            self.run.log_pr_curve(
                name="pr_test", precision=x, recall=y, average_precision=0.6, step=1
            )
            self.run.log_curve(name="curve_test", x=x, y=y, annotation=0.6, step=1)
        assert log_curves.call_count == 3
        self.event_logger.flush()
        assert (
            os.path.exists(get_asset_path(self.run_path, kind=V1ArtifactKind.CURVE))
            is False
        )
        assert (
            os.path.exists(get_event_path(self.run_path, kind=V1ArtifactKind.CURVE))
            is True
        )

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CURVE, name="roc_test"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(
            kind=V1ArtifactKind.CURVE, name="roc_test", data=events_file
        )
        assert len(results.df.values) == 1

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CURVE, name="pr_test"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(
            kind=V1ArtifactKind.CHART, name="pr_test", data=events_file
        )
        assert len(results.df.values) == 1

        events_file = get_event_path(
            self.run_path, kind=V1ArtifactKind.CURVE, name="curve_test"
        )
        assert os.path.exists(events_file) is True
        results = V1Events.read(
            kind=V1ArtifactKind.CHART, name="curve_test", data=events_file
        )
        assert len(results.df.values) == 1
