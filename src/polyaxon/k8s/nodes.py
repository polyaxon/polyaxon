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

from polyaxon.constants.globals import UNKNOWN
from polyaxon.utils.units import to_cpu_value, to_memory_bytes


class NodeLifeCycle:
    UNKNOWN = UNKNOWN
    READY = "ready"
    NOT_READY = "notReady"
    DELETED = "deleted"

    CHOICES = (
        (UNKNOWN, UNKNOWN),
        (READY, READY),
        (NOT_READY, NOT_READY),
        (DELETED, DELETED),
    )


class NodeParser:
    @staticmethod
    def get_status(node) -> str:
        status = [c.status for c in node.status.conditions if c.type == "Ready"][0]
        if status == "True":
            return NodeLifeCycle.READY
        if status == "False":
            return NodeLifeCycle.NOT_READY
        return NodeLifeCycle.UNKNOWN

    @staticmethod
    def get_n_gpus(node) -> int:
        if "gpu" not in node.status.allocatable:
            return 0
        return int(node.status.allocatable.get("nvidia.com/gpu", 0))

    @staticmethod
    def get_cpu(node) -> float:
        cpu = node.status.allocatable["cpu"]
        return to_cpu_value(cpu)

    @classmethod
    def get_memory(cls, node) -> int:
        return to_memory_bytes(node.status.allocatable["memory"])

    @staticmethod
    def get_runtime(node) -> str:
        return node.status.node_info.container_runtime_version

    @staticmethod
    def get_schedulable_state(node) -> bool:
        return not node.spec.unschedulable

    @staticmethod
    def get_addresses(node) -> str:
        return node.status.addresses
