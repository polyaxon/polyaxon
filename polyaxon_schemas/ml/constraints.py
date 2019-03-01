# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema


class MaxNormSchema(BaseSchema):
    max_value = fields.Int(default=2, missing=2)
    axis = fields.Int(default=0, missing=0)

    @staticmethod
    def schema_config():
        return MaxNormConfig


class MaxNormConfig(BaseConfig):
    """MaxNorm weight constraint.

    Constrains the weights incident to each hidden unit
    to have a norm less than or equal to a desired value.

    Args:
        m: the maximum norm for the incoming weights.
        axis: integer, axis along which to calculate weight norms.
            For instance, in a `Dense` layer the weight matrix
            has shape `(input_dim, output_dim)`,
            set `axis` to `0` to constrain each weight vector
            of length `(input_dim,)`.
            In a `Conv2D` layer with `data_format="channels_last"`,
            the weight tensor has shape
            `(rows, cols, input_depth, output_depth)`,
            set `axis` to `[0, 1, 2]`
            to constrain the weights of each filter tensor of size
            `(rows, cols, input_depth)`.

    References:
        - [Dropout: A Simple Way to Prevent Neural Networks from Overfitting
          Srivastava, Hinton, et al.
          2014](http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)

    Polyaxonfile usage:

    Using the default values

    ```yaml
    MaxNorm:
    ```

    Using custom values

    ```yaml
    MaxNorm:
      max_value: 3
      axis: 0
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint: MaxNorm
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint:
        MaxNorm:
          max_value: 3
    ```
    """
    IDENTIFIER = 'MaxNorm'
    SCHEMA = MaxNormSchema

    def __init__(self, max_value=2, axis=0):
        self.max_value = max_value
        self.axis = axis


class NonNegSchema(BaseSchema):
    w = fields.Float()

    @staticmethod
    def schema_config():
        return NonNegConfig


class NonNegConfig(BaseConfig):
    """Constrains the weights to be non-negative.

    Polyaxonfile usage:

    ```yaml
    NonNeg:
      w: 0.2
    ```

    Example with layer:

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint:
        NonNeg:
          w: 0.2
    ```
    """
    IDENTIFIER = 'NonNeg'
    SCHEMA = NonNegSchema

    def __init__(self, w):
        self.w = w


class UnitNormSchema(BaseSchema):
    axis = fields.Int(default=0, missing=0)

    @staticmethod
    def schema_config():
        return UnitNormConfig


class UnitNormConfig(BaseConfig):
    """Constrains the weights incident to each hidden unit to have unit norm.

    Args:
        axis: integer, axis along which to calculate weight norms.
            For instance, in a `Dense` layer the weight matrix
            has shape `(input_dim, output_dim)`,
            set `axis` to `0` to constrain each weight vector
            of length `(input_dim,)`.
            In a `Conv2D` layer with `data_format="channels_last"`,
            the weight tensor has shape
            `(rows, cols, input_depth, output_depth)`,
            set `axis` to `[0, 1, 2]`
            to constrain the weights of each filter tensor of size
            `(rows, cols, input_depth)`.

    Polyaxonfile usage:

    Using the default values

    ```yaml
    UnitNorm:
    ```

    Using custom values

    ```yaml
    UnitNorm:
      axis: 1
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint: UnitNorm
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint:
        UnitNorm:
          axis: 1
    ```
    """
    IDENTIFIER = 'UnitNorm'
    SCHEMA = UnitNormSchema

    def __init__(self, axis=0):
        self.axis = axis


class MinMaxNormSchema(BaseSchema):
    min_value = fields.Float(default=0., missing=0.)
    max_value = fields.Float(default=1., missing=1.)
    rate = fields.Float(default=1., missing=1.)
    axis = fields.Int(default=0, missing=0)

    @staticmethod
    def schema_config():
        return MinMaxNormConfig


class MinMaxNormConfig(BaseConfig):
    """MinMaxNorm weight constraint.

    Constrains the weights incident to each hidden unit
    to have the norm between a lower bound and an upper bound.

    Args:
        min_value: the minimum norm for the incoming weights.
        max_value: the maximum norm for the incoming weights.
        rate: rate for enforcing the constraint: weights will be
            rescaled to yield
            `(1 - rate) * norm + rate * norm.clip(min_value, max_value)`.
            Effectively, this means that rate=1.0 stands for strict
            enforcement of the constraint, while rate<1.0 means that
            weights will be rescaled at each step to slowly move
            towards a value inside the desired interval.
        axis: integer, axis along which to calculate weight norms.
            For instance, in a `Dense` layer the weight matrix
            has shape `(input_dim, output_dim)`,
            set `axis` to `0` to constrain each weight vector
            of length `(input_dim,)`.
            In a `Conv2D` layer with `dim_ordering="channels_last"`,
            the weight tensor has shape
            `(rows, cols, input_depth, output_depth)`,
            set `axis` to `[0, 1, 2]`
            to constrain the weights of each filter tensor of size
            `(rows, cols, input_depth)`.

    Polyaxonfile usage:

    Using the default values

    ```yaml
    MinMaxNorm:
    ```

    Using custom values

    ```yaml
    MinMaxNorm:
      min_value: 0.1
      max_value: 0.8
      rate: 0.9
      axis: 0
    ```

    Example with layer

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint: MinMaxNorm
    ```

    or

    ```yaml
    Conv2D:
      filters: 10
      kernel_size: 8
      kernel_constraint:
        MinMaxNorm:
          min_value: 0.1
          max_value: 0.8
          rate: 0.9
          axis: 0
    ```
    """
    IDENTIFIER = 'MinMaxNorm'
    SCHEMA = MinMaxNormSchema

    def __init__(self, min_value=0.0, max_value=1.0, rate=1.0, axis=0):
        self.min_value = min_value
        self.max_value = max_value
        self.rate = rate
        self.axis = axis


class ConstraintSchema(BaseMultiSchema):
    __multi_schema_name__ = 'constraint'
    __configs__ = {
        MaxNormConfig.IDENTIFIER: MaxNormConfig,
        NonNegConfig.IDENTIFIER: NonNegConfig,
        UnitNormConfig.IDENTIFIER: UnitNormConfig,
        MinMaxNormConfig.IDENTIFIER: MinMaxNormConfig,
    }
