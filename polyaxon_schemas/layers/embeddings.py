# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import InitializerSchema, UniformInitializerConfig
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class EmbeddingSchema(BaseLayerSchema):
    input_dim = fields.Int()
    output_dim = fields.Int()
    embeddings_initializer = fields.Nested(InitializerSchema, allow_none=True)
    embeddings_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    activity_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    embeddings_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    mask_zero = fields.Bool(default=False, missing=False)
    input_length = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return EmbeddingConfig(**data)


class EmbeddingConfig(BaseLayerConfig):
    IDENTIFIER = 'Embedding'
    SCHEMA = EmbeddingSchema

    def __init__(self,
                 input_dim,
                 output_dim,
                 embeddings_initializer=UniformInitializerConfig(),
                 embeddings_regularizer=None,
                 activity_regularizer=None,
                 embeddings_constraint=None,
                 mask_zero=False,
                 input_length=None,
                 **kwargs):
        super(EmbeddingConfig, self).__init__(**kwargs)
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.embeddings_initializer = embeddings_initializer
        self.embeddings_regularizer = embeddings_regularizer
        self.activity_regularizer = activity_regularizer
        self.embeddings_constraint = embeddings_constraint
        self.mask_zero = mask_zero
        self.input_length = input_length
