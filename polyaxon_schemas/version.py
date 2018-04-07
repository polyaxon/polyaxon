# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class BaseVersionSchema(Schema):
    latest_version = fields.Str()
    min_version = fields.Str()


class BaseVersionConfig(BaseConfig):
    def __init__(self, latest_version, min_version):
        self.latest_version = latest_version
        self.min_version = min_version


class CliVersionSchema(BaseVersionSchema):
    class Meta:
        ordered = True

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
        min_version: the version below which cli should fail.
    """
    SCHEMA = CliVersionSchema
    IDENTIFIER = 'cli_version'


class PlatformVersionSchema(BaseVersionSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PlatformVersionConfig(**data)

    @post_dump
    def unmake(self, data):
        return PlatformVersionConfig.remove_reduced_attrs(data)


class PlatformVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest platform available on helm.
        min_version: the version below which platform should fail.
    """
    SCHEMA = PlatformVersionSchema
    IDENTIFIER = 'platform_version'


class LibVersionSchema(BaseVersionSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LibVersionConfig(**data)

    @post_dump
    def unmake(self, data):
        return LibVersionConfig.remove_reduced_attrs(data)


class LibVersionConfig(BaseVersionConfig):
    """
    Args:
        latest_version: the newest lib available on PIP.
        min_version: the version below which lib should fail.
    """
    SCHEMA = LibVersionSchema
    IDENTIFIER = 'lib_version'


class ChartVersionSchema(Schema):
    version = fields.Str()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ChartVersionConfig(**data)

    @post_dump
    def unmake(self, data):
        return ChartVersionConfig.remove_reduced_attrs(data)


class ChartVersionConfig(BaseConfig):
    """
    Args:
        version: the current installed chart version.
    """
    SCHEMA = ChartVersionSchema
    IDENTIFIER = 'chart_version'

    def __init__(self, version):
        self.version = version
