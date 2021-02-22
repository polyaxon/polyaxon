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

import time
import traceback

from polyaxon.client import RunClient
from polyaxon.client.impersonate import impersonate
from polyaxon.exceptions import PolyaxonClientException, PolyaxonContainerException


def create_auth_context():
    try:
        run_client = RunClient()
    except PolyaxonClientException as e:
        raise PolyaxonContainerException(e)

    retry = 1
    done = False
    exp = None
    while not done and retry <= 3:
        try:
            impersonate(
                owner=run_client.owner,
                project=run_client.project,
                run_uuid=run_client.run_uuid,
                client=run_client.client,
            )
            print("Auth context initialized.")
            return
        except PolyaxonClientException as e:
            retry += 1
            print("Could not establish connection, retrying ...")
            exp = "Polyaxon auth initialized failed authenticating the operation: {}\n{}".format(
                repr(e), traceback.format_exc()
            )
            time.sleep(retry)
    run_client.log_failed(reason="AuthContext", message=exp)
    raise PolyaxonContainerException("Init job did not succeed authenticating job.")
