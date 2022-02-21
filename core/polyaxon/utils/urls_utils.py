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

from urllib.parse import urljoin, urlparse


def validate_url(url):
    if not url.startswith(("http://", "https://")):
        return False
    parsed = urlparse(url)
    if not parsed.hostname:
        return False
    return True


def get_owner_url(owner: str) -> str:
    return "/{}".format(owner)


def get_project_url(unique_name: str) -> str:
    values = unique_name.split(".")
    return "{}/{}".format(get_owner_url(values[0]), values[1])


def get_owner_project_url(owner: str, project_name: str) -> str:
    return "{}/{}".format(get_owner_url(owner), project_name)


def get_fqn_run_url(unique_name: str) -> str:
    values = unique_name.split(".")
    project_url = get_owner_project_url(owner=values[0], project_name=values[1])
    return f"{project_url}/runs/{values[-1]}"


def get_run_url(owner: str, project_name: str, run_uuid: str) -> str:
    project_url = get_owner_project_url(owner=owner, project_name=project_name)
    return f"{project_url}/runs/{run_uuid}"


def get_run_health_url(unique_name: str) -> str:
    run_url = get_fqn_run_url(unique_name=unique_name)
    return f"{run_url}/_heartbeat"


def get_proxy_run_url(
    service: str,
    namespace: str,
    owner: str,
    project: str,
    run_uuid: str,
    subpath: str = None,
) -> str:
    url_path = "{namespace}/{owner}/{project}/runs/{run_uuid}".format(
        namespace=namespace,
        owner=owner,
        project=project,
        run_uuid=run_uuid,
    )
    if subpath:
        url_path = "{}/{}".format(url_path, subpath)
    return urljoin(service.rstrip() + "/", url_path.lstrip("/"))


def get_run_reconcile_url(unique_name: str) -> str:
    run_url = get_fqn_run_url(unique_name=unique_name)
    return "{}/_reconcile".format(run_url)


URL_FORMAT = "{protocol}://{domain}{path}"
