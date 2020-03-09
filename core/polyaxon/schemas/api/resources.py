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

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.fields import UUID


class ContainerGPUResourcesSchema(BaseSchema):
    index = fields.Int()
    uuid = fields.Str()
    name = fields.Str()
    minor = fields.Int()
    bus_id = fields.Str()
    serial = fields.Str()
    temperature_gpu = fields.Int()
    utilization_gpu = fields.Int()
    power_draw = fields.Int()
    power_limit = fields.Int()
    memory_free = fields.Int()
    memory_used = fields.Int()
    memory_total = fields.Int()
    memory_utilization = fields.Int()
    processes = fields.List(fields.Dict(), allow_none=True)

    @staticmethod
    def schema_config():
        return ContainerGPUResourcesConfig


class ContainerGPUResourcesConfig(BaseConfig):
    SCHEMA = ContainerGPUResourcesSchema
    IDENTIFIER = "ContainerGPUResources"
    MEM_SIZE_ATTRIBUTES = ["memory_free", "memory_used", "memory_total"]

    def __init__(
        self,
        index,
        uuid,
        name,
        minor,
        bus_id,
        serial,
        temperature_gpu,
        utilization_gpu,
        power_draw,
        power_limit,
        memory_free,
        memory_used,
        memory_total,
        memory_utilization,
        processes=None,
    ):
        self.index = index
        self.uuid = uuid
        self.name = name
        self.minor = minor
        self.bus_id = bus_id
        self.serial = serial
        self.temperature_gpu = temperature_gpu
        self.utilization_gpu = utilization_gpu
        self.power_draw = power_draw
        self.power_limit = power_limit
        self.memory_free = memory_free
        self.memory_used = memory_used
        self.memory_total = memory_total
        self.memory_utilization = memory_utilization
        self.processes = processes


class ContainerResourcesSchema(BaseSchema):
    job_uuid = UUID()
    experiment_uuid = UUID()
    job_name = fields.Str()
    container_id = fields.Str()
    n_cpus = fields.Int()
    cpu_percentage = fields.Float()
    percpu_percentage = fields.List(fields.Float(), allow_none=True)
    memory_used = fields.Int()
    memory_limit = fields.Int()
    gpu_resources = fields.Nested(
        ContainerGPUResourcesSchema, many=True, allow_none=True
    )

    @staticmethod
    def schema_config():
        return ContainerResourcesConfig


class ContainerResourcesConfig(BaseConfig):
    SCHEMA = ContainerResourcesSchema
    IDENTIFIER = "ContainerResources"
    PERCENT_ATTRIBUTES = ["cpu_percentage"]
    MEM_SIZE_ATTRIBUTES = ["memory_used", "memory_limit"]

    def __init__(
        self,
        job_uuid,
        experiment_uuid,
        job_name,
        container_id,
        n_cpus,
        cpu_percentage,
        percpu_percentage,
        memory_used,
        memory_limit,
        gpu_resources=None,
    ):
        self.job_uuid = job_uuid
        self.experiment_uuid = experiment_uuid
        self.job_name = job_name
        self.container_id = container_id
        self.n_cpus = n_cpus
        self.cpu_percentage = cpu_percentage
        self.percpu_percentage = percpu_percentage
        self.memory_used = memory_used
        self.memory_limit = memory_limit
        self.gpu_resources = gpu_resources
