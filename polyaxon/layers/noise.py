# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

try:
    from tensorflow.python.keras._impl.keras.layers import noise
except ImportError:
    from tensorflow.contrib.keras.python.keras.layers import noise

from polyaxon_schemas.layers.noise import (
    GaussianNoiseConfig,
    GaussianDropoutConfig,
    AlphaDropoutConfig,
)

from polyaxon.libs.base_object import BaseObject


class GaussianNoise(BaseObject, noise.GaussianNoise):
    CONFIG = GaussianNoiseConfig
    __doc__ = GaussianNoiseConfig.__doc__


class GaussianDropout(BaseObject, noise.GaussianDropout):
    CONFIG = GaussianDropoutConfig
    __doc__ = GaussianDropoutConfig.__doc__


class AlphaDropout(BaseObject, noise.AlphaDropout):
    CONFIG = AlphaDropoutConfig
    __doc__ = AlphaDropoutConfig.__doc__


NOISE_LAYERS = OrderedDict([
    (GaussianNoise.CONFIG.IDENTIFIER, GaussianNoise),
    (GaussianDropout.CONFIG.IDENTIFIER, GaussianDropout),
    (AlphaDropout.CONFIG.IDENTIFIER, AlphaDropout),
])
