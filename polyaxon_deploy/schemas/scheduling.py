# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class NodeSelectorsSchema(BaseSchema):
    core = fields.Dict(allow_none=True)
    experiments = fields.Dict(allow_none=True)
    jobs = fields.Dict(allow_none=True)
    builds = fields.Dict(allow_none=True)
    tensorboards = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return NodeSelectorsConfig


class NodeSelectorsConfig(BaseConfig):
    SCHEMA = NodeSelectorsSchema
    REDUCED_ATTRIBUTES = ['core', 'experiments', 'jobs', 'builds', 'tensorboards']

    def __init__(self,
                 core=None,
                 experiments=None,
                 jobs=None,
                 builds=None,
                 tensorboards=None):
        self.core = core
        self.experiments = experiments
        self.jobs = jobs
        self.builds = builds
        self.tensorboards = tensorboards


class AffinitySchema(BaseSchema):
    core = fields.Dict(allow_none=True)
    experiments = fields.Dict(allow_none=True)
    jobs = fields.Dict(allow_none=True)
    builds = fields.Dict(allow_none=True)
    tensorboards = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return AffinityConfig


class AffinityConfig(BaseConfig):
    SCHEMA = AffinitySchema
    REDUCED_ATTRIBUTES = ['core', 'experiments', 'jobs', 'builds', 'tensorboards']

    def __init__(self,
                 core=None,
                 experiments=None,
                 jobs=None,
                 builds=None,
                 tensorboards=None):
        self.core = core
        self.experiments = experiments
        self.jobs = jobs
        self.builds = builds
        self.tensorboards = tensorboards


class TolerationsSchema(BaseSchema):
    resourcesDaemon = fields.List(fields.Dict(allow_none=True), allow_none=True)
    core = fields.List(fields.Dict(allow_none=True), allow_none=True)
    experiments = fields.List(fields.Dict(allow_none=True), allow_none=True)
    jobs = fields.List(fields.Dict(allow_none=True), allow_none=True)
    builds = fields.List(fields.Dict(allow_none=True), allow_none=True)
    tensorboards = fields.List(fields.Dict(allow_none=True), allow_none=True)

    @staticmethod
    def schema_config():
        return TolerationsConfig


class TolerationsConfig(BaseConfig):
    SCHEMA = TolerationsSchema
    REDUCED_ATTRIBUTES = [
        'resourcesDaemon',
        'core',
        'experiments',
        'jobs',
        'builds',
        'tensorboards'
    ]

    def __init__(self,  # noqa
                 resourcesDaemon=None,
                 core=None,
                 experiments=None,
                 jobs=None,
                 builds=None,
                 tensorboards=None):
        self.resourcesDaemon = resourcesDaemon
        self.core = core
        self.experiments = experiments
        self.jobs = jobs
        self.builds = builds
        self.tensorboards = tensorboards
