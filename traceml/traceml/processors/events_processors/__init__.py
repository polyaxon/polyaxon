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

from typing import Dict

from polyaxon.utils.path_utils import copy_file_or_dir_path, copy_file_path
from traceml.events import (
    V1EventArtifact,
    V1EventAudio,
    V1EventDataframe,
    V1EventImage,
    V1EventModel,
    V1EventVideo,
)
from traceml.processors.events_processors.events_audio_processors import audio
from traceml.processors.events_processors.events_charts_processors import (
    altair_chart,
    bokeh_chart,
    mpl_plotly_chart,
    plotly_chart,
)
from traceml.processors.events_processors.events_image_processors import (
    convert_to_HWC,
    draw_boxes,
    encoded_image,
    ensure_matplotlib_figure,
    figure_to_image,
    figures_to_images,
    image,
    image_boxes,
    make_grid,
    make_image,
    save_image,
)
from traceml.processors.events_processors.events_metrics_processors import (
    confusion_matrix,
    curve,
    histogram,
    metric,
    metrics_dict_to_list,
    np_histogram,
    pr_curve,
    roc_auc_curve,
    sklearn_pr_curve,
    sklearn_roc_auc_curve,
)
from traceml.processors.events_processors.events_models_processors import model_to_str
from traceml.processors.events_processors.events_video_processors import (
    make_video,
    prepare_video,
    video,
)

try:
    import numpy as np
except ImportError:
    np = None


def dataframe_path(
    from_path: str,
    asset_path: str,
    content_type: str = None,
    asset_rel_path: str = None,
) -> V1EventDataframe:
    copy_file_path(from_path, asset_path)
    return V1EventDataframe(
        path=asset_rel_path or asset_path, content_type=content_type
    )


def model_path(
    from_path: str,
    asset_path: str,
    framework: str = None,
    spec: Dict = None,
    asset_rel_path: str = None,
) -> V1EventModel:
    copy_file_or_dir_path(from_path, asset_path)
    return V1EventModel(
        path=asset_rel_path or asset_path, framework=framework, spec=spec
    )


def artifact_path(
    from_path: str, asset_path: str, kind: str, asset_rel_path: str = None
) -> V1EventArtifact:
    copy_file_or_dir_path(from_path, asset_path)
    return V1EventArtifact(kind=kind, path=asset_rel_path or asset_path)


def image_path(
    from_path: str, asset_path: str, asset_rel_path: str = None
) -> V1EventImage:
    copy_file_path(from_path, asset_path)
    return V1EventImage(path=asset_rel_path or asset_path)


def video_path(
    from_path: str, asset_path: str, content_type=None, asset_rel_path: str = None
) -> V1EventVideo:
    copy_file_path(from_path, asset_path)
    return V1EventVideo(path=asset_rel_path or asset_path, content_type=content_type)


def audio_path(
    from_path: str, asset_path: str, content_type=None, asset_rel_path: str = None
) -> V1EventAudio:
    copy_file_path(from_path, asset_path)
    return V1EventAudio(path=asset_rel_path or asset_path, content_type=content_type)
