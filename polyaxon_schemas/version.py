# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class BaseVersionSchema(BaseSchema):
    latest_version = fields.Str()
    min_version = fields.Str()


class BaseVersionConfig(BaseConfig):
    def __init__(self, latest_version, min_version):
        self.latest_version = latest_version
        self.min_version = min_version


class CliVersionSchema(BaseVersionSchema):
    @staticmethod
    def schema_config():
        return CliVersionConfig


class CliVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest cli available on PIP.
        min_version: the version below which cli should fail.
    """
    SCHEMA = CliVersionSchema
    IDENTIFIER = 'cli_version'


class PlatformVersionSchema(BaseVersionSchema):
    @staticmethod
    def schema_config():
        return PlatformVersionConfig


class PlatformVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest platform available on helm.
        min_version: the version below which platform should fail.
    """
    SCHEMA = PlatformVersionSchema
    IDENTIFIER = 'platform_version'


class LibVersionSchema(BaseVersionSchema):
    @staticmethod
    def schema_config():
        return LibVersionConfig


class LibVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest lib available on PIP.
        min_version: the version below which lib should fail.
    """
    SCHEMA = LibVersionSchema
    IDENTIFIER = 'lib_version'


class ChartVersionSchema(BaseSchema):
    version = fields.Str()

    @staticmethod
    def schema_config():
        return ChartVersionConfig


class ChartVersionConfig(BaseConfig):
    """
    Args:
        version: the current installed chart version.
    """
    SCHEMA = ChartVersionSchema
    IDENTIFIER = 'chart_version'

    def __init__(self, version):
        self.version = version
