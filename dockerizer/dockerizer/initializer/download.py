#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

import logging

from .utils import ensure_path

_logger = logging.getLogger('polyaxon.dockerizer')


def download(job: 'Job', extract_path: str, download_file: str, commit: str):
    ensure_path(extract_path)

    repo_file = job.client.project.download_repo(
        username=job.username,
        project_name=job.project_name,
        commit=commit,
        filename=download_file,
        untar=True,
        delete_tar=True,
        extract_path=extract_path
    )
    if not repo_file:
        job.failed(message='Could not download code to build the image.')
        return False

    return True
