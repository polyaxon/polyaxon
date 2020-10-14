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

from polyaxon.agents import converter
from polyaxon.agents.spawners.spawner import Spawner


def start(
    content: str,
    owner_name: str,
    project_name: str,
    run_name: str,
    run_kind: str,
    run_uuid: str,
    namespace: str,
    in_cluster: bool = None,
    default_auth: bool = False,
):
    resource = converter.convert(
        owner_name=owner_name,
        project_name=project_name,
        run_name=run_name,
        run_uuid=run_uuid,
        content=content,
        default_auth=default_auth,
    )
    Spawner(namespace=namespace, in_cluster=in_cluster).create(
        run_uuid=run_uuid, run_kind=run_kind, resource=resource
    )


def apply(
    content: str,
    owner_name: str,
    project_name: str,
    run_name: str,
    run_kind: str,
    run_uuid: str,
    namespace: str,
    in_cluster: bool = None,
    default_auth: bool = False,
):
    resource = converter.convert(
        owner_name=owner_name,
        project_name=project_name,
        run_name=run_name,
        run_uuid=run_uuid,
        content=content,
        default_auth=default_auth,
    )
    Spawner(namespace=namespace, in_cluster=in_cluster).apply(
        run_uuid=run_uuid, run_kind=run_kind, resource=resource
    )


def stop(run_kind: str, run_uuid: str, namespace: str, in_cluster: bool = None):
    Spawner(namespace=namespace, in_cluster=in_cluster).stop(
        run_uuid=run_uuid, run_kind=run_kind
    )


def clean(run_kind: str, run_uuid: str, namespace: str, in_cluster: bool = None):
    Spawner(namespace=namespace, in_cluster=in_cluster).clean(
        run_uuid=run_uuid, run_kind=run_kind
    )


def make_and_create(
    content: str,
    owner_name: str,
    project_name: str,
    run_name: str,
    run_kind: str,
    run_uuid: str,
    namespace: str,
    in_cluster: bool = None,
):
    resource = converter.make_and_convert(
        owner_name=owner_name,
        project_name=project_name,
        run_name=run_name,
        run_uuid=run_uuid,
        content=content,
    )

    Spawner(namespace=namespace, in_cluster=in_cluster).create(
        run_uuid=run_uuid, run_kind=run_kind, resource=resource
    )
