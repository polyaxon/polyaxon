# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from polyaxon.layers.advanced_activations import (
    ADVANCED_ACTIVATION_LAYERS,
    LeakyReLU,
    PReLU,
    ELU,
    ThresholdedReLU,
)
from polyaxon.layers.convolutional import (
    CONVOLUTIONAL_LAYERS,
    Conv1D,
    Conv2D,
    Conv3D,
    Conv2DTranspose,
    Conv3DTranspose,
    SeparableConv2D,
    UpSampling1D,
    UpSampling2D,
    UpSampling3D,
    ZeroPadding1D,
    ZeroPadding2D,
    ZeroPadding3D,
    Cropping1D,
    Cropping2D,
    Cropping3D,
)
from polyaxon.layers.convolutional_recurrent import (
    CONVOLUTIONAL_RECURRENT_LAYERS,
    ConvRecurrent2D,
    ConvLSTM2D,
)
from polyaxon.layers.core import (
    CORE_LAYERS,
    Masking,
    Dropout,
    SpatialDropout1D,
    SpatialDropout2D,
    SpatialDropout3D,
    Activation,
    Reshape,
    Permute,
    Flatten,
    RepeatVector,
    Dense,
    ActivityRegularization,
)
from polyaxon.layers.embeddings import (
    EMBEDDING_LAYERS,
    Embedding,
)
from polyaxon.layers.local import (
    LOCAL_LAYERS,
    LocallyConnected1D,
    LocallyConnected2D,
)
from polyaxon.layers.merge import (
    MERGE_LAYERS,
    Add,
    Multiply,
    Average,
    Maximum,
    Concatenate,
    Dot,
)
from polyaxon.layers.noise import (
    NOISE_LAYERS,
    GaussianNoise,
    GaussianDropout,
    AlphaDropout,
)
from polyaxon.layers.normalizations import (
    NORMALIZATION_LAYERS,
    BatchNormalization,
)
from polyaxon.layers.pooling import (
    POOLING_LAYERS,
    AveragePooling1D,
    MaxPooling1D,
    AveragePooling2D,
    MaxPooling2D,
    AveragePooling3D,
    MaxPooling3D,
    GlobalAveragePooling1D,
    GlobalMaxPooling1D,
    GlobalAveragePooling2D,
    GlobalMaxPooling2D,
    GlobalAveragePooling3D,
    GlobalMaxPooling3D,
)
from polyaxon.layers.recurrent import (
    RECURRENT_LAYERS,
    Recurrent,
    SimpleRNN,
    GRU,
    LSTM,
)
from polyaxon.layers.wrappers import (
    WRAPPER_LAYERS,
    Wrapper,
    TimeDistributed,
    Bidirectional,
)

LAYERS = OrderedDict()
LAYERS.update(ADVANCED_ACTIVATION_LAYERS)
LAYERS.update(CONVOLUTIONAL_LAYERS)
LAYERS.update(CONVOLUTIONAL_RECURRENT_LAYERS)
LAYERS.update(CORE_LAYERS)
LAYERS.update(EMBEDDING_LAYERS)
LAYERS.update(LOCAL_LAYERS)
LAYERS.update(MERGE_LAYERS)
LAYERS.update(NOISE_LAYERS)
LAYERS.update(NORMALIZATION_LAYERS)
LAYERS.update(POOLING_LAYERS)
LAYERS.update(RECURRENT_LAYERS)
LAYERS.update(WRAPPER_LAYERS)
