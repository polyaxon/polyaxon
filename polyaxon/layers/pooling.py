# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import pooling

from polyaxon_schemas.layers.pooling import (
    AveragePooling1DConfig,
    MaxPooling1DConfig,
    AveragePooling2DConfig,
    MaxPooling2DConfig,
    AveragePooling3DConfig,
    MaxPooling3DConfig,
    GlobalAveragePooling1DConfig,
    GlobalMaxPooling1DConfig,
    GlobalAveragePooling2DConfig,
    GlobalMaxPooling2DConfig,
    GlobalAveragePooling3DConfig,
    GlobalMaxPooling3DConfig
)

from polyaxon.libs.base_object import BaseObject


class AveragePooling1D(BaseObject, pooling.AveragePooling1D):
    CONFIG = AveragePooling1DConfig
    __doc__ = pooling.AveragePooling1D.__doc__


class MaxPooling1D(BaseObject, pooling.MaxPooling1D):
    CONFIG = MaxPooling1DConfig
    __doc__ = pooling.MaxPooling1D.__doc__


class AveragePooling2D(BaseObject, pooling.AveragePooling2D):
    CONFIG = AveragePooling2DConfig
    __doc__ = pooling.AveragePooling2D.__doc__


class MaxPooling2D(BaseObject, pooling.MaxPooling2D):
    CONFIG = MaxPooling2DConfig
    __doc__ = pooling.MaxPooling2D.__doc__


class AveragePooling3D(BaseObject, pooling.AveragePooling3D):
    CONFIG = AveragePooling3DConfig
    __doc__ = pooling.AveragePooling3D.__doc__


class MaxPooling3D(BaseObject, pooling.MaxPooling3D):
    CONFIG = MaxPooling3DConfig
    __doc__ = pooling.MaxPooling3D.__doc__


class GlobalAveragePooling1D(BaseObject, pooling.GlobalAveragePooling1D):
    CONFIG = GlobalAveragePooling1DConfig
    __doc__ = pooling.GlobalAveragePooling1D.__doc__


class GlobalMaxPooling1D(BaseObject, pooling.GlobalMaxPooling1D):
    CONFIG = GlobalMaxPooling1DConfig
    __doc__ = pooling.GlobalMaxPooling1D.__doc__


class GlobalAveragePooling2D(BaseObject, pooling.GlobalAveragePooling2D):
    CONFIG = GlobalAveragePooling2DConfig
    __doc__ = pooling.GlobalAveragePooling2D.__doc__


class GlobalMaxPooling2D(BaseObject, pooling.GlobalMaxPooling2D):
    CONFIG = GlobalMaxPooling2DConfig
    __doc__ = pooling.GlobalMaxPooling2D.__doc__


class GlobalAveragePooling3D(BaseObject, pooling.GlobalAveragePooling3D):
    CONFIG = GlobalAveragePooling3DConfig
    __doc__ = pooling.GlobalAveragePooling3D.__doc__


class GlobalMaxPooling3D(BaseObject, pooling.GlobalMaxPooling3D):
    CONFIG = GlobalMaxPooling3DConfig
    __doc__ = pooling.GlobalMaxPooling3D.__doc__


POOLING_LAYERS = OrderedDict([
    (AveragePooling1D.CONFIG.IDENTIFIER, AveragePooling1D),
    (MaxPooling1D.CONFIG.IDENTIFIER, MaxPooling1D),
    (AveragePooling2D.CONFIG.IDENTIFIER, AveragePooling2D),
    (MaxPooling2D.CONFIG.IDENTIFIER, MaxPooling2D),
    (AveragePooling3D.CONFIG.IDENTIFIER, AveragePooling3D),
    (MaxPooling3D.CONFIG.IDENTIFIER, MaxPooling3D),
    (GlobalAveragePooling1D.CONFIG.IDENTIFIER, GlobalAveragePooling1D),
    (GlobalMaxPooling1D.CONFIG.IDENTIFIER, GlobalMaxPooling1D),
    (GlobalAveragePooling2D.CONFIG.IDENTIFIER, GlobalAveragePooling2D),
    (GlobalMaxPooling2D.CONFIG.IDENTIFIER, GlobalMaxPooling2D),
    (GlobalAveragePooling3D.CONFIG.IDENTIFIER, GlobalAveragePooling3D),
    (GlobalMaxPooling3D.CONFIG.IDENTIFIER, GlobalMaxPooling3D),
])
