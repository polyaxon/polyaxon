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

# coding: utf-8
from __future__ import absolute_import, division, print_function

import time

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.client import PolyaxonClient
from polyaxon.exceptions import PolyaxonClientException


def _get_run_statuses(owner, project, run_uuid, last_status=None):
    try:
        polyaxon_client = PolyaxonClient()
        response = polyaxon_client.runs_v1.get_run_statuses(owner, project, run_uuid)
        if not last_status:
            return response.status, response.status_conditions
        if last_status == response.status:
            return [last_status, []]

        conditions = []
        for c in reversed(response.status_conditions):
            if c.type == last_status:
                break
            conditions.append(c)

        return response.status, reversed(conditions)

    except (ApiException, HTTPError) as e:
        raise PolyaxonClientException(e)


def get_run_statuses(owner, project, run_uuid, watch=False):
    if not watch:
        yield _get_run_statuses(owner, project, run_uuid)
        return

    last_status = None
    is_done = {"failed", "upstream_failed", "stopped", "skipped", "succeeded"}
    while last_status not in is_done:
        last_status, conditions = _get_run_statuses(
            owner, project, run_uuid, last_status
        )
        yield last_status, conditions
        time.sleep(settings.CLIENT_CONFIG.watch_interval)
