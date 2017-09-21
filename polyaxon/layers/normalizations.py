# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import normalization

from polyaxon_schemas.layers.normalization import BatchNormalizationConfig

from polyaxon.libs.base_object import BaseObject


class BatchNormalization(BaseObject, normalization.BatchNormalization):
    CONFIG = BatchNormalizationConfig


NORMALIZATION_LAYERS = OrderedDict([
    (BatchNormalization.CONFIG.IDENTIFIER, BatchNormalization),
    # ('LocalResponseNormalization', LocalResponseNormalization),
    # ('L2Normalization', L2Normalization)
])
