# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema


class BaseEnvironmentSchema(BaseSchema):
    env_id = fields.Str()

    @staticmethod
    def schema_config():
        return BaseEnvironmentConfig


class BaseEnvironmentConfig(BaseConfig):
    def __init__(self, env_id):
        self.env_id = env_id


class GymEnvironmentSchema(BaseEnvironmentSchema):

    @staticmethod
    def schema_config():
        return GymEnvironmentConfig


class GymEnvironmentConfig(BaseEnvironmentConfig):
    IDENTIFIER = 'Gym'
    SCHEMA = GymEnvironmentSchema


class RegularizerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'environment'
    __configs__ = {
        GymEnvironmentConfig.IDENTIFIER: GymEnvironmentConfig,
    }
