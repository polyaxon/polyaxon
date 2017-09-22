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


class NonNeg(BaseObject, constraints.NonNeg):
    CONFIG = NonNegConfig


class UnitNorm(BaseObject, constraints.UnitNorm):
   CONFIG = UnitNormConfig


class MinMaxNorm(BaseObject, constraints.MinMaxNorm):
    CONFIG = MinMaxNormConfig


CONSTRAINTS = {
    MaxNorm.CONFIG.IDENTIFIER: MaxNorm,
    NonNeg.CONFIG.IDENTIFIER: NonNeg,
    UnitNorm.CONFIG.IDENTIFIER: UnitNorm,
    MinMaxNorm.CONFIG.IDENTIFIER: MinMaxNorm,
}
