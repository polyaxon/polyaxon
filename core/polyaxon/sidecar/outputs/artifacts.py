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

from datetime import datetime
from typing import Optional

from polyaxon.containers.contexts import CONTEXT_MOUNT_ARTIFACTS_FORMAT
from polyaxon.stores.manager import get_artifacts_connection, upload_file_or_dir
from polyaxon.utils.tz_utils import now


def sync_artifacts(last_check: Optional[datetime], run_uuid: str):
    new_check = now()
    connection_type = get_artifacts_connection()
    path_from = CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(run_uuid)
    # check if there's a path to sync
    if os.path.exists(path_from):
        path_to = os.path.join(connection_type.store_path, run_uuid)

        upload_file_or_dir(
            path_from=path_from,
            path_to=path_to,
            is_file=False,
            workers=5,
            last_time=last_check,
            connection_type=connection_type,
            exclude=["plxlogs"],
        )

    return new_check
