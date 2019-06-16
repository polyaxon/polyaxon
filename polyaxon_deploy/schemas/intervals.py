# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class IntervalsSchema(BaseSchema):
    experimentsScheduler = fields.Int(default=None)
    experimentsSync = fields.Int(default=None)
    clustersUpdateSystemInfo = fields.Int(default=None)
    clustersUpdateSystemNodes = fields.Int(default=None)
    pipelinesScheduler = fields.Int(default=None)
    operationsDefaultRetryDelay = fields.Int(default=None)
    operationsMaxRetryDelay = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return IntervalsConfig


class IntervalsConfig(BaseConfig):
    SCHEMA = IntervalsSchema
    REDUCED_ATTRIBUTES = [
        'experimentsScheduler',
        'experimentsSync',
        'clustersUpdateSystemInfo',
        'clustersUpdateSystemNodes',
        'pipelinesScheduler',
        'operationsDefaultRetryDelay',
        'operationsMaxRetryDelay',
    ]

    def __init__(self,  # noqa
                 experimentsScheduler=None,
                 experimentsSync=None,
                 clustersUpdateSystemInfo=None,
                 clustersUpdateSystemNodes=None,
                 pipelinesScheduler=None,
                 operationsDefaultRetryDelay=None,
                 operationsMaxRetryDelay=None):
        self.experimentsScheduler = experimentsScheduler
        self.experimentsSync = experimentsSync
        self.clustersUpdateSystemInfo = clustersUpdateSystemInfo
        self.clustersUpdateSystemNodes = clustersUpdateSystemNodes
        self.pipelinesScheduler = pipelinesScheduler
        self.operationsDefaultRetryDelay = operationsDefaultRetryDelay
        self.operationsMaxRetryDelay = operationsMaxRetryDelay
