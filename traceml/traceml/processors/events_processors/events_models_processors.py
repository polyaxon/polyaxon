#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from polyaxon.utils.path_utils import copy_file_or_dir_path
from traceml.events import V1EventModel
from traceml.logger import logger

try:
    import numpy as np
except ImportError:
    np = None


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


def _model_to_str(model):
    filetype = "txt"
    if hasattr(model, "to_json"):
        model = model.model.to_json()
        filetype = "json"
    elif hasattr(model, "to_yaml"):
        model = model.to_yaml()
        filetype = "yaml"

    try:
        return str(model), filetype
    except Exception as e:
        logger.warning("Could not convert model to a string. Error: %s" % e)


def model_to_str(model):
    # Tensorflow Graph Definition
    if type(model).__name__ == "Graph":
        try:
            from google.protobuf import json_format

            graph_def = model.as_graph_def()
            model = json_format.MessageToJson(graph_def, sort_keys=True)
        except Exception as e:  # noqa
            logger.warning(
                "Could not convert Tensorflow graph to JSON %s", e, exc_info=True
            )

    return _model_to_str(model)
