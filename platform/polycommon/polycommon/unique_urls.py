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


def get_user_url(username: str) -> str:
    return "/{}".format(username)


def get_project_url(unique_name: str) -> str:
    values = unique_name.split(".")
    return "{}/{}".format(get_user_url(values[0]), values[1])


def get_user_project_url(username: str, project_name: str) -> str:
    return "{}/{}".format(get_user_url(username), project_name)


def get_run_url(unique_name: str) -> str:
    values = unique_name.split(".")
    project_url = get_user_project_url(username=values[0], project_name=values[1])
    return f"{project_url}/runs/{values[-1]}"


def get_run_health_url(unique_name: str) -> str:
    run_url = get_run_url(unique_name=unique_name)
    return f"{run_url}/_heartbeat"


def get_run_reconcile_url(unique_name: str) -> str:
    run_url = get_run_url(unique_name=unique_name)
    return "{}/_reconcile".format(run_url)
