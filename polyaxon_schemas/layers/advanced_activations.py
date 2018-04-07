# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, post_dump, post_load

from polyaxon_schemas.constraints import ConstraintSchema
from polyaxon_schemas.initializations import InitializerSchema, ZerosInitializerConfig
from polyaxon_schemas.layers.base import BaseLayerConfig, BaseLayerSchema
from polyaxon_schemas.regularizations import RegularizerSchema
from polyaxon_schemas.utils import ObjectOrListObject


class LeakyReLUSchema(BaseLayerSchema):
    alpha = fields.Float(default=0.3, missing=0.3)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return LeakyReLUConfig(**data)

    @post_dump
    def unmake(self, data):
        return LeakyReLUConfig.remove_reduced_attrs(data)


class LeakyReLUConfig(BaseLayerConfig):
    """Leaky version of a Rectified Linear Unit.

    It allows a small gradient when the unit is not active:
    `f(x) = alpha * x for x < 0`,
    `f(x) = x for x >= 0`.

    Args:
        alpha: float >= 0. Negative slope coefficient.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as the input.

    Polyaxonfile usage:

    ```yaml
    LeakyReLU:
        alpha: 0.2
    ```
    """
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
    def make(self, data):
        return PReLUConfig(**data)

    @post_dump
    def unmake(self, data):
        return PReLUConfig.remove_reduced_attrs(data)


class PReLUConfig(BaseLayerConfig):
    """Parametric Rectified Linear Unit.

    It follows:
    `f(x) = alpha * x for x < 0`,
    `f(x) = x for x >= 0`,
    where `alpha` is a learned array with the same shape as x.

    Args:
        alpha_initializer: initializer function for the weights.
        alpha_regularizer: regularizer for the weights.
        alpha_constraint: constraint for the weights.
        shared_axes: the axes along which to share learnable
            parameters for the activation function.
            For example, if the incoming feature maps
            are from a 2D convolution
            with output shape `(batch, height, width, channels)`,
            and you wish to share parameters across space
            so that each filter only has one set of parameters,
            set `shared_axes=[1, 2]`.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as the input.

    Polyaxonfile usage:

    ```yaml
    PReLU:
      alpha_initializer:
        ZerosInitializer:
      alpha_regularizer:
        L2:
         l: 0.01
      shared_axes: [1, 2]
    ```
    """
    IDENTIFIER = 'PReLU'
    SCHEMA = PReLUSchema

    def __init__(self,
                 alpha_initializer=ZerosInitializerConfig(),
                 alpha_regularizer=None,
                 alpha_constraint=None,
                 shared_axes=None,
                 **kwargs):
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
    def make(self, data):
        return ELUConfig(**data)

    @post_dump
    def unmake(self, data):
        return ELUConfig.remove_reduced_attrs(data)


class ELUConfig(BaseLayerConfig):
    """Exponential Linear Unit.

    It follows:
    `f(x) =  alpha * (exp(x) - 1.) for x < 0`,
    `f(x) = x for x >= 0`.

    Args:
        alpha: scale for the negative factor.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as the input.

    Polyaxonfile usage:

    ```yaml
    ELU:
      alpha:0.1
    ```
    """
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
    def make(self, data):
        return ThresholdedReLUConfig(**data)

    @post_dump
    def unmake(self, data):
        return ThresholdedReLUConfig.remove_reduced_attrs(data)


class ThresholdedReLUConfig(BaseLayerConfig):
    """Thresholded Rectified Linear Unit.

    It follows:
    `f(x) = x for x > theta`,
    `f(x) = 0 otherwise`.

    Args:
        theta: float >= 0. Threshold location of activation.

    Input shape:
        Arbitrary. Use the keyword argument `input_shape`
        (tuple of integers, does not include the samples axis)
        when using this layer as the first layer in a model.

    Output shape:
        Same shape as the input.

    Polyaxonfile usage:

    ```yaml
    ThresholdedReLU:
      theta:0.1
    ```
    """
    IDENTIFIER = 'ThresholdedReLU'
    SCHEMA = ThresholdedReLUSchema

    def __init__(self, theta=1.0, **kwargs):
        super(ThresholdedReLUConfig, self).__init__(**kwargs)
        self.theta = theta
