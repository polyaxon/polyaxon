# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig


class CliVersionSchema(Schema):
    latest_version = fields.Str()
    min_version = fields.Str()

    @post_load
    def make(self, data):
        return CliVersionConfig(**data)

    @post_dump
    def unmake(self, data):
        return CliVersionConfig.remove_reduced_attrs(data)


class CliVersionConfig(BaseConfig):
    """
    Args:
        latest_version: the newest cli available on PIP.
        min_version: the version below which CLI should fail.
    """
    SCHEMA = CliVersionSchema
    IDENTIFIER = 'version'

    def __init__(self, latest_version, min_version):
        self.latest_version = latest_version
        self.min_version = min_version
