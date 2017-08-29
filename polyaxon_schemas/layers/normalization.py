# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import (
    InitializerSchema,
    OnesInitializerConfig,
    ZerosInitializerConfig,
)
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class BatchNormalizationSchema(BaseLayerSchema):
    axis = fields.Int(default=-1, missing=-1)
    momentum = fields.Float(default=0.99, missing=0.99)
    epsilon = fields.Float(default=1e-3, missing=1e-3)
    center = fields.Bool(default=True, missing=True)
    scale = fields.Bool(default=True, missing=True)
    beta_initializer = fields.Nested(InitializerSchema, allow_none=True)
    gamma_initializer = fields.Nested(InitializerSchema, allow_none=True)
    moving_mean_initializer = fields.Nested(InitializerSchema, allow_none=True)
    moving_variance_initializer = fields.Nested(InitializerSchema, allow_none=True)
    beta_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    gamma_regularizer = fields.Nested(RegularizerSchema, allow_none=True)
    beta_constraint = fields.Nested(ConstraintSchema, allow_none=True)
    gamma_constraint = fields.Nested(ConstraintSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return BatchNormalizationConfig(**data)


class BatchNormalizationConfig(BaseLayerConfig):
    IDENTIFIER = 'BatchNormalization'
    SCHEMA = BatchNormalizationSchema

    def __init__(self,
                 axis=-1,
                 momentum=0.99,
                 epsilon=1e-3,
                 center=True,
                 scale=True,
                 beta_initializer=ZerosInitializerConfig(),
                 gamma_initializer=OnesInitializerConfig(),
                 moving_mean_initializer=ZerosInitializerConfig(),
                 moving_variance_initializer=OnesInitializerConfig(),
                 beta_regularizer=None,
                 gamma_regularizer=None,
                 beta_constraint=None,
                 gamma_constraint=None,
                 **kwargs):
        super(BatchNormalizationConfig, self).__init__(**kwargs)
        self.axis = axis
        self.momentum = momentum
        self.epsilon = epsilon
        self.center = center
        self.scale = scale
        self.beta_initializer = beta_initializer
        self.gamma_initializer = gamma_initializer
        self.moving_mean_initializer = moving_mean_initializer
        self.moving_variance_initializer = moving_variance_initializer
        self.beta_regularizer = beta_regularizer
        self.gamma_regularizer = gamma_regularizer
        self.beta_constraint = beta_constraint
        self.gamma_constraint = gamma_constraint
