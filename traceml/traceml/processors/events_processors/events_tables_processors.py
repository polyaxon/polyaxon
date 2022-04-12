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

from polyaxon.utils.path_utils import copy_file_path
from traceml.events import V1EventDataframe

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
