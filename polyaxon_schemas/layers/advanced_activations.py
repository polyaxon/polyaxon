# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_load

from polyaxon_schemas.utils import ObjectOrListObject
from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import InitializerSchema, ZerosInitializerConfig
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.layers.base import BaseLayerSchema, BaseLayerConfig


class LeakyReLUSchema(BaseLayerSchema):
    alpha = fields.Float(default=0.3, missing=0.3)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return LeakyReLUConfig(**data)


class LeakyReLUConfig(BaseLayerConfig):
    IDENTIFIER = 'LeakyReLU'
    SCHEMA = LeakyReLUSchema

    def __init__(self, alpha=0.3, **kwargs):
        super(LeakyReLUConfig, self).__init__(**kwargs)
        self.alpha = alpha


class PReLUSchema(BaseLayerSchema):
    alpha_initializer = fields.Nested(InitializerSchema, default=None, missing=None)
    alpha_regularizer = fields.Nested(RegularizerSchema, default=None, missing=None)
    alpha_constraint = fields.Nested(ConstraintSchema, default=None, missing=None)
    shared_axes = ObjectOrListObject(fields.Int, default=None, missing=None)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return PReLUConfig(**data)


class PReLUConfig(BaseLayerConfig):
    IDENTIFIER = 'PReLU'
    SCHEMA = PReLUSchema

    def __init__(self, alpha_initializer=ZerosInitializerConfig(), alpha_regularizer=None,
                 alpha_constraint=None, shared_axes=None, **kwargs):
        super(PReLUConfig, self).__init__(**kwargs)
        self.alpha_initializer = alpha_initializer
        self.alpha_regularizer = alpha_regularizer
        self.alpha_constraint = alpha_constraint
        self.shared_axes = shared_axes


class ELUSchema(BaseLayerSchema):
    alpha = fields.Float(default=1.0, missing=1.0)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ELUConfig(**data)


class ELUConfig(BaseLayerConfig):
    IDENTIFIER = 'ELU'
    SCHEMA = ELUSchema

    def __init__(self, alpha=0.1, **kwargs):
        super(ELUConfig, self).__init__(**kwargs)
        self.alpha = alpha


class ThresholdedReLUSchema(BaseLayerSchema):
    theta = fields.Float(default=1.0, missing=1.0)

    class Meta:
        ordered = True

    @post_load
    def make_load(self, data):
        return ThresholdedReLUConfig(**data)


class ThresholdedReLUConfig(BaseLayerConfig):
    IDENTIFIER = 'ThresholdedReLU'
    SCHEMA = ThresholdedReLUSchema

    def __init__(self, theta=1.0, **kwargs):
        super(ThresholdedReLUConfig, self).__init__(**kwargs)
        self.theta = theta
