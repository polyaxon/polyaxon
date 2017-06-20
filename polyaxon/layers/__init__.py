# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from .convolutional import (
    CONV_LAYERS,
    AvgPool1d,
    AvgPool2d,
    AvgPool3d,
    Conv1d,
    Conv2d,
    Conv2dTranspose,
    Conv3d,
    Conv3dTranspose,
    GlobalAvgPool,
    GlobalMaxPool,
    HighwayConv1d,
    HighwayConv2d,
    MaxPool1d,
    MaxPool2d,
    MaxPool3d,
    ResidualBlock,
    ResidualBottleneck,
    Upsample2d,
    Upscore
)
from .core import (
    CORE_LAYERS,
    Dropout,
    Flatten,
    FullyConnected,
    GaussianNoise,
    Highway,
    Merge,
    OneHotEncoding,
    Reshape,
    SingleUnit,
    Slice
)
from .embedding import EMBEDDING_LAYERS, Embedding
from .normalizations import (
    NORMALIZATION_LAYERS,
    BatchNormalization,
    L2Normalization,
    LocalResponseNormalization
)
from .recurrent import (
    RNN_LAYERS,
    GRU,
    LSTM,
    BasicLSTMCell,
    BasicRNNCell,
    BidirectionalRNN,
    GRUCell,
    SimpleRNN
)

LAYERS = OrderedDict()
LAYERS.update(CORE_LAYERS)
LAYERS.update(CONV_LAYERS)
LAYERS.update(RNN_LAYERS)
LAYERS.update(EMBEDDING_LAYERS)
LAYERS.update(RNN_LAYERS)
LAYERS.update(NORMALIZATION_LAYERS)
