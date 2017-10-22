# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.contrib.keras.python.keras import constraints

from polyaxon_schemas.constraints import (
    MaxNormConfig,
    NonNegConfig,
    UnitNormConfig,
    MinMaxNormConfig,
)

from polyaxon.libs.base_object import BaseObject


class MaxNorm(BaseObject, constraints.MaxNorm):
    CONFIG = MaxNormConfig
    __doc__ = constraints.MaxNorm.__doc__


class NonNeg(BaseObject, constraints.NonNeg):
    CONFIG = NonNegConfig
    __doc__ = constraints.NonNeg.__doc__


class UnitNorm(BaseObject, constraints.UnitNorm):
    CONFIG = UnitNormConfig
    __doc__ = constraints.UnitNorm.__doc__


class MinMaxNorm(BaseObject, constraints.MinMaxNorm):
    CONFIG = MinMaxNormConfig
    __doc__ = constraints.MinMaxNorm.__doc__


CONSTRAINTS = {
    MaxNorm.CONFIG.IDENTIFIER: MaxNorm,
    NonNeg.CONFIG.IDENTIFIER: NonNeg,
    UnitNorm.CONFIG.IDENTIFIER: UnitNorm,
    MinMaxNorm.CONFIG.IDENTIFIER: MinMaxNorm,
}
