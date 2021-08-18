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

import os

from polyaxon import settings
from polyaxon.utils.path_utils import create_tarfile, get_files_in_path


def tar_dir(download_path: str) -> str:
    outputs_files = get_files_in_path(download_path)
    tar_base_name = os.path.basename(download_path)
    tar_name = "{}.tar.gz".format(tar_base_name)
    target_path = os.path.join(settings.CLIENT_CONFIG.archive_root, tar_name)
    create_tarfile(files=outputs_files, tar_path=target_path, relative_to=download_path)
    return target_path
