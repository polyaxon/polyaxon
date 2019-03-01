# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema, BaseSchema


class BaseRegularizerSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    collect = fields.Bool(default=True, missing=True)

    @staticmethod
    def schema_config():
        return BaseRegularizerConfig


class BaseRegularizerConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self, name, collect=True):
        self.name = name
        self.collect = collect


class L1RegularizerSchema(BaseRegularizerSchema):
    l = fields.Float(default=0.01, missing=0.01)  # noqa

    @staticmethod
    def schema_config():
        return L1RegularizerConfig


class L1RegularizerConfig(BaseRegularizerConfig):
    """Regularizer for L1 regularization.

    Args:
        l: Float; regularization factor.

    Polyaxonfile usage:

    ```yaml
    Dense:
      units: 32
      kernel_regularizer: L1
    ```

    or

    ```yaml
    Dense:
      units: 32
      kernel_regularizer:
        L1:
          l: 0.2
    ```

    or

    ```yaml
    Dense:
      units: 32
      kernel_regularizer:
        L1: {l: 0.2}
    ```
    """
    IDENTIFIER = 'L1'
    SCHEMA = L1RegularizerSchema

    def __init__(self, l=0.01, name='L1Regularizer', collect=True):  # noqa
        self.l = l  # noqa
        super(L1RegularizerConfig, self).__init__(name, collect)


class L2RegularizerSchema(BaseRegularizerSchema):
    l = fields.Float(default=0.01, missing=0.01)  # noqa

    @staticmethod
    def schema_config():
        return L2RegularizerConfig


class L2RegularizerConfig(BaseRegularizerConfig):
    """Regularizer for L2 regularization.

    Args:
        l: Float; regularization factor.

    Polyaxonfile usage:

    ```yaml
    Dense:
      units: 32
      kernel_regularizer: L2
    ```

    or

    ```yaml
    Dense:
      units: 32
      kernel_regularizer:
        L2:
          l: 0.2
    ```

    or

    ```yaml
    Dense:
      units: 32
      kernel_regularizer:
        L2: {l: 0.2}
    ```
    """
    IDENTIFIER = 'L2'
    SCHEMA = L2RegularizerSchema

    def __init__(self, l=0.01, name='L2Regularizer', collect=True):  # noqa
        self.l = l  # noqa
        super(L2RegularizerConfig, self).__init__(name, collect)


class L1L2RegularizerSchema(BaseRegularizerSchema):
    l1 = fields.Float(default=0.01, missing=0.01)
    l2 = fields.Float(default=0.01, missing=0.01)

    @staticmethod
    def schema_config():
        return L1L2RegularizerConfig


class L1L2RegularizerConfig(BaseRegularizerConfig):
    """Regularizer for L1 and L2 regularization.

    Args:
        l1: Float; L1 regularization factor.
        l2: Float; L2 regularization factor.

    Polyaxonfile usage:

    ```yaml
    Dense:
      units: 32
      kernel_regularizer: L1L2
    ```

    or

    ```yaml
    Dense:
      units: 32
      kernel_regularizer:
        L1L2:
          l1: 0.2
          l2: 0.1
    ```

    or

    ```yaml
    Dense:
      units: 32
      kernel_regularizer:
        L1L2: {l1: 0.2, l2: 0.1}
    ```
    """
    IDENTIFIER = 'L1L2'
    SCHEMA = L1L2RegularizerSchema

    def __init__(self, l1=0.01, l2=0.01, name='L1L2Regularizer', collect=True):
        self.l1 = l1
        self.l2 = l2
        super(L1L2RegularizerConfig, self).__init__(name, collect)


class RegularizerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'regularizer'
    __configs__ = {
        L1RegularizerConfig.IDENTIFIER: L1RegularizerConfig,
        L2RegularizerConfig.IDENTIFIER: L2RegularizerConfig,
        L1L2RegularizerConfig.IDENTIFIER: L1L2RegularizerConfig,
    }
    __support_snake_case__ = True
