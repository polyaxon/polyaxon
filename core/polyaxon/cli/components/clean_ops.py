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

import click


@click.command()
@click.option("--namespace", type=str)
@click.option("--in-cluster", is_flag=True, default=False)
@click.option("--delete", is_flag=True, default=False)
def clean_ops(namespace, in_cluster, delete):
    """clean-ops command."""
    from polyaxon.k8s.custom_resources import operation
    from polyaxon.k8s.manager import K8SManager

    if not namespace:
        raise ValueError("namespace is required!")

    manager = K8SManager(namespace=namespace, in_cluster=in_cluster)

    def _patch_op():
        retry = 0
        while retry < 2:
            try:
                manager.update_custom_object(
                    name=op["metadata"]["name"],
                    group=operation.GROUP,
                    version=operation.API_VERSION,
                    plural=operation.PLURAL,
                    body={"metadata": {"finalizers": None}},
                )
                return
            except Exception as e:
                print("Exception %s", e)
                print("retrying")
                time.sleep(0.1)
                retry += 1

    def _delete_op():
        retry = 0
        while retry < 2:
            try:
                manager.delete_custom_object(
                    name=op["metadata"]["name"],
                    group=operation.GROUP,
                    version=operation.API_VERSION,
                    plural=operation.PLURAL,
                )
                return
            except Exception as e:
                print("Exception %s", e)
                print("retrying")
                time.sleep(0.1)
                retry += 1

    ops = manager.list_custom_objects(
        group=operation.GROUP,
        version=operation.API_VERSION,
        plural=operation.PLURAL,
    )

    for op in ops:
        _patch_op()
        if delete:
            _delete_op()
