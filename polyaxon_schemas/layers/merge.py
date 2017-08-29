# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import post_load

from polyaxon_schemas.base import BaseMultiSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class AddSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AddConfig(**data)


class AddConfig(BaseLayerConfig):
    IDENTIFIER = 'Add'
    SCHEMA = AddSchema


class MultiplySchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MultiplyConfig(**data)


class MultiplyConfig(BaseLayerConfig):
    IDENTIFIER = 'Multiply'
    SCHEMA = MultiplySchema


class AverageSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return AverageConfig(**data)


class AverageConfig(BaseLayerConfig):
    IDENTIFIER = 'Average'
    SCHEMA = AverageSchema


class MaximumSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return MaximumConfig(**data)


class MaximumConfig(BaseLayerConfig):
    IDENTIFIER = 'Maximum'
    SCHEMA = MaximumSchema


class ConcatenateSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ConcatenateConfig(**data)


class ConcatenateConfig(BaseLayerConfig):
    IDENTIFIER = 'Concatenate'
    SCHEMA = ConcatenateSchema


class DotSchema(BaseLayerSchema):

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return DotConfig(**data)


class DotConfig(BaseLayerConfig):
    IDENTIFIER = 'Dot'
    SCHEMA = DotSchema


class MergeSchema(BaseMultiSchema):
    __multi_schema_name__ = 'Merge'
    __configs__ = {
        AddConfig.IDENTIFIER: AddConfig,
        MultiplyConfig.IDENTIFIER: MultiplyConfig,
        AverageConfig.IDENTIFIER: AverageConfig,
        MaximumConfig.IDENTIFIER: MaximumConfig,
        ConcatenateConfig.IDENTIFIER: ConcatenateConfig,
        DotConfig.IDENTIFIER: DotConfig,
    }


class MergeConfig(BaseLayerConfig):
    IDENTIFIER = 'Merge'
    SCHEMA = MergeSchema
