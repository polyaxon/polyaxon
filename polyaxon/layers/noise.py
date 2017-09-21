# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import noise

from polyaxon_schemas.layers.noise import (
    GaussianNoiseConfig,
    GaussianDropoutConfig,
    AlphaDropoutConfig,
)

from polyaxon.libs.base_object import BaseObject


class GaussianNoise(BaseObject, noise.GaussianNoise):
    CONFIG = GaussianNoiseConfig


class GaussianDropout(BaseObject, noise.GaussianDropout):
    CONFIG = GaussianDropoutConfig


class AlphaDropout(BaseObject, noise.AlphaDropout):
    CONFIG = AlphaDropoutConfig


NOISE_LAYERS = OrderedDict([
    (GaussianNoise.CONFIG.IDENTIFIER, GaussianNoise),
    (GaussianDropout.CONFIG.IDENTIFIER, GaussianDropout),
    (AlphaDropout.CONFIG.IDENTIFIER, AlphaDropout),
])
