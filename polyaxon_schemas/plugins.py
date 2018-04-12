# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class PluginJobSchema(Schema):
    config = fields.Dict(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PluginJobConfig(**data)

    @post_dump
    def unmake(self, data):
        return PluginJobConfig.remove_reduced_attrs(data)


class PluginJobConfig(BaseConfig):
    SCHEMA = PluginJobSchema
    IDENTIFIER = 'plugin_job'

    def __init__(self, config=None):
        self.config = config  # The json compiled content of this experiment
