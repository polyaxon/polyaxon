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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.cli.getters.project import get_project_or_local
from polyaxon.managers.run import RunManager


def get_run_or_local(run_uuid=None):
    return run_uuid or RunManager.get_config_or_raise().uuid


def get_project_run_or_local(project=None, run_uuid=None):
    user, project_name = get_project_or_local(project)
    run_uuid = get_run_or_local(run_uuid)
    return user, project_name, run_uuid
