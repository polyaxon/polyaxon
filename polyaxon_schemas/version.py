# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig


class BaseVersionSchema(Schema):
    latest_version = fields.Str()
    min_version = fields.Str()


class BaseVersionConfig(BaseConfig):

    def __init__(self, latest_version, min_version):
        self.latest_version = latest_version
        self.min_version = min_version


class CliVersionSchema(BaseVersionSchema):

    @post_load
    def make(self, data):
        return CliVersionConfig(**data)

    @post_dump
    def unmake(self, data):
        return CliVersionConfig.remove_reduced_attrs(data)


class CliVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest cli available on PIP.
        min_version: the version below which CLI should fail.
    """
    SCHEMA = CliVersionSchema
    IDENTIFIER = 'cli_version'


class PlatformVersionSchema(BaseVersionSchema):
    @post_load
    def make(self, data):
        return PlatformVersionConfig(**data)

    @post_dump
    def unmake(self, data):
        return PlatformVersionConfig.remove_reduced_attrs(data)


class PlatformVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest cli available on PIP.
        min_version: the version below which CLI should fail.
    """
    SCHEMA = PlatformVersionSchema
    IDENTIFIER = 'platform_version'
