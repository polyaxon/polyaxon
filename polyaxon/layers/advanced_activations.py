# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict


from tensorflow.contrib.keras.python.keras.layers import advanced_activations

from polyaxon_schemas.layers.advanced_activations import (
    LeakyReLUConfig,
    PReLUConfig,
    ELUConfig,
    ThresholdedReLUConfig,
)

from polyaxon.libs.base_object import BaseObject


class LeakyReLU(BaseObject, advanced_activations.LeakyReLU):
    CONFIG = LeakyReLUConfig
    __doc__ = LeakyReLUConfig.__doc__


class PReLU(BaseObject, advanced_activations.PReLU):
    CONFIG = PReLUConfig
    __doc__ = PReLUConfig.__doc__


class ELU(BaseObject, advanced_activations.ELU):
    CONFIG = ELUConfig
    __doc__ = ELUConfig.__doc__


class ThresholdedReLU(BaseObject, advanced_activations.ThresholdedReLU):
    CONFIG = ThresholdedReLUConfig
    __doc__ = ThresholdedReLUConfig.__doc__


ADVANCED_ACTIVATION_LAYERS = OrderedDict([
    (LeakyReLU.CONFIG.IDENTIFIER, LeakyReLU),
    (PReLU.CONFIG.IDENTIFIER, PReLU),
    (ELU.CONFIG.IDENTIFIER, ELU),
    (ThresholdedReLU.CONFIG.IDENTIFIER, ThresholdedReLU),
])
