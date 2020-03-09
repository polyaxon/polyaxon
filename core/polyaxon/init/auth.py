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

import time

from polyaxon.client.impersonate import impersonate
from polyaxon.env_vars.getters import get_run_info
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException


def create_auth_context():
    try:
        owner, project, run_uuid = get_run_info()
    except PolyaxonClientException as e:
        raise PolyaxonContainerException(e)

    retry = 1
    done = False
    while not done and retry <= 3:
        try:
            impersonate(owner=owner, project=project, run_uuid=run_uuid)
            print("Auth context initialized.")
            return
        except PolyaxonClientException:
            retry += 1
            print("Could not establish connection, retrying ...")
            time.sleep(1 * retry)

    raise PolyaxonContainerException("Init job did not succeed authenticating job.")
