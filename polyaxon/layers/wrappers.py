# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import wrappers

from polyaxon_schemas.layers.wrappers import (
    WrapperConfig,
    TimeDistributedConfig,
    BidirectionalConfig,
)

from polyaxon.libs.base_object import BaseObject


class Wrapper(BaseObject, wrappers.Wrapper):
    CONFIG = WrapperConfig
    __doc__ = wrappers.Wrapper.__doc__


class TimeDistributed(BaseObject, wrappers.TimeDistributed):
    CONFIG = TimeDistributedConfig
    __doc__ = wrappers.TimeDistributed.__doc__


class Bidirectional(BaseObject, wrappers.Bidirectional):
    CONFIG = BidirectionalConfig
    __doc__ = wrappers.Bidirectional.__doc__


WRAPPER_LAYERS = OrderedDict([
    (Wrapper.CONFIG.IDENTIFIER, Wrapper),
    (TimeDistributed.CONFIG.IDENTIFIER, TimeDistributed),
    (Bidirectional.CONFIG.IDENTIFIER, Bidirectional),
])
