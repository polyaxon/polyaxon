# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import local

from polyaxon_schemas.layers.local import LocallyConnected1DConfig, LocallyConnected2DConfig

from polyaxon.libs.base_object import BaseObject


class LocallyConnected1D(BaseObject, local.LocallyConnected1D):
    CONFIG = LocallyConnected1DConfig


class LocallyConnected2D(BaseObject, local.LocallyConnected2D):
    CONFIG = LocallyConnected2DConfig


LOCAL_LAYERS = OrderedDict([
    (LocallyConnected1D.CONFIG.IDENTIFIER, LocallyConnected1D),
    (LocallyConnected2D.CONFIG.IDENTIFIER, LocallyConnected2D),
])
