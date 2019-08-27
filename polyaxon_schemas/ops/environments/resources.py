# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import INCLUDE, fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import FloatOrStr, IntOrStr


class K8SResourcesEntrySchema(BaseSchema):
    cpu = FloatOrStr(allow_none=True)
    memory = IntOrStr(allow_none=True)
    gpu = fields.Int(allow_none=True)
    tpu = fields.Int(allow_none=True)

    class Meta:
        unknown = INCLUDE

    @staticmethod
    def schema_config():
        return K8SResourcesEntryConfig


class K8SResourcesEntryConfig(BaseConfig):
    SCHEMA = K8SResourcesEntrySchema
    REDUCED_ATTRIBUTES = ["cpu", "memory", "gpu", "tpu"]

    def __init__(self, cpu=None, memory=None, gpu=None, tpu=None):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.tpu = tpu


class K8SContainerResourcesSchema(BaseSchema):
    limits = fields.Nested(K8SResourcesEntrySchema, allow_none=True)
    requests = fields.Nested(K8SResourcesEntrySchema, allow_none=True)

    @staticmethod
    def schema_config():
        return K8SContainerResourcesConfig


class K8SContainerResourcesConfig(BaseConfig):
    """
    K8S container resources config.

    Args:
        limits: `K8SResourcesEntry`.
        requests: `K8SResourcesEntry`.
    """

    IDENTIFIER = "resources"
    SCHEMA = K8SContainerResourcesSchema
    REDUCED_ATTRIBUTES = ["limits", "requests"]

    def __init__(self, limits=None, requests=None):
        self.limits = limits
        self.requests = requests

    @staticmethod
    def from_resources_entry(resources):  # pylint:disable=too-many-branches
        if resources is None:
            return None

        limits = {}
        requests = {}
        if resources.cpu:
            if resources.cpu.limits:
                limits["cpu"] = resources.cpu.limits
            if resources.cpu.requests:
                requests["cpu"] = resources.cpu.requests
        if resources.memory:
            if resources.memory.limits:
                memory = int(resources.memory.limits)
                if memory != resources.memory.limits:
                    memory = resources.memory.limits
                limits["memory"] = "{}Mi".format(memory)
            if resources.memory.requests:
                memory = int(resources.memory.requests)
                if memory != resources.memory.requests:
                    memory = resources.memory.requests
                requests["memory"] = "{}Mi".format(memory)
        if resources.gpu:
            if resources.gpu.limits:
                limits["gpu"] = int(resources.gpu.limits)
            if resources.gpu.requests:
                requests["gpu"] = int(resources.gpu.requests)
        if resources.tpu:
            if resources.tpu.limits:
                limits["tpu"] = int(resources.tpu.limits)
            if resources.tpu.requests:
                requests["tpu"] = int(resources.tpu.requests)
        resource_results = {}
        if limits:
            resource_results["limits"] = limits
        if requests:
            resource_results["requests"] = requests
        return resource_results


class K8SResourcesSchema(BaseSchema):
    limits = fields.Float(allow_none=True)
    requests = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return K8SResourcesConfig


class K8SResourcesConfig(BaseConfig):
    """
    K8S resources config.

    Args:
        limits: `float`.
        requests: `float`.
    """

    IDENTIFIER = "resources"
    SCHEMA = K8SResourcesSchema
    REDUCED_ATTRIBUTES = ["limits", "requests"]

    def __init__(self, limits=None, requests=None):
        self.limits = limits
        self.requests = requests

    def __add__(self, other):
        if not other:
            return self

        if self.requests:
            if other.requests:
                self.requests += other.requests
        elif other.requests:
            self.requests = other.requests

        if self.limits:
            if other.limits:
                self.limits += other.limits
        elif other.limits:
            self.limits = other.limits

        return self


class PodResourcesSchema(BaseSchema):
    cpu = fields.Nested(K8SResourcesSchema, allow_none=True)
    memory = fields.Nested(K8SResourcesSchema, allow_none=True)
    gpu = fields.Nested(K8SResourcesSchema, allow_none=True)
    tpu = fields.Nested(K8SResourcesSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return PodResourcesConfig


class PodResourcesConfig(BaseConfig):
    """
    Pod resources config.

    Args:
        cpu: `K8SResourcesConfig`.
        memory: `K8SResourcesConfig`.
        gpu: `K8SResourcesConfig`.
        tpu: `K8SResourcesConfig`.
    """

    IDENTIFIER = "pod_resources"
    SCHEMA = PodResourcesSchema
    REDUCED_ATTRIBUTES = ["cpu", "memory", "gpu", "tpu"]

    def __init__(self, cpu=None, memory=None, gpu=None, tpu=None):
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.tpu = tpu

    def __add__(self, other):  # pylint:disable=too-many-branches
        if not other:
            return self

        if self.cpu:
            if other.cpu:
                self.cpu += other.cpu
        elif other.cpu:
            self.cpu = K8SResourcesConfig()
            self.cpu += other.cpu

        if self.memory:
            if other.memory:
                self.memory += other.memory
        elif other.memory:
            self.memory = K8SResourcesConfig()
            self.memory += other.memory

        if self.gpu:
            if other.gpu:
                self.gpu += other.gpu
        elif other.gpu:
            self.gpu = K8SResourcesConfig()
            self.gpu += other.gpu

        if self.tpu:
            if other.tpu:
                self.tpu += other.tpu
        elif other.tpu:
            self.tpu = K8SResourcesConfig()
            self.tpu += other.tpu
        return self
