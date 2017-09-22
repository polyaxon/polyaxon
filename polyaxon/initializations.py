# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.contrib.keras.python.keras import initializers
from tensorflow.python.ops import init_ops

from polyaxon_schemas import initializations

from polyaxon.libs.base_object import BaseObject


class Zeros(BaseObject, init_ops.Zeros):
    CONFIG = initializations.ZerosInitializerConfig


class Ones(BaseObject, init_ops.Ones):
    CONFIG = initializations.OnesInitializerConfig


class Constant(BaseObject, init_ops.Constant):
    CONFIG = initializations.ConstantInitializerConfig


class Uniform(BaseObject, init_ops.RandomUniform):
    CONFIG = initializations.UniformInitializerConfig


class Normal(BaseObject, init_ops.RandomNormal):
    CONFIG = initializations.NormalInitializerConfig


class TruncatedNormal(BaseObject, init_ops.TruncatedNormal):
    CONFIG = initializations.TruncatedNormalInitializerConfig


class VarianceScaling(BaseObject, init_ops.VarianceScaling):
    CONFIG = initializations.VarianceScalingInitializerConfig


class Orthogonal(BaseObject, init_ops.Orthogonal):
    CONFIG = initializations.OrthogonalInitializerConfig


class Identity(BaseObject, initializers.Identity):
    CONFIG = initializations.IdentityInitializerConfig


class GlorotUniform(BaseObject, init_ops.Initializer):
    CONFIG = initializations.GlorotUniformInitializerConfig

    def __init__(self, seed=None):
        self.seed = seed

    def __call__(self, shape, dtype=None, partition_info=None):
        return initializers.glorot_uniform(seed=self.seed)(shape, dtype)


class GlorotNormal(BaseObject, init_ops.Initializer):
    CONFIG = initializations.GlorotNormalInitializerConfig

    def __init__(self, seed=None):
        self.seed = seed

    def __call__(self, shape, dtype=None, partition_info=None):
        return initializers.glorot_normal(seed=self.seed)(shape, dtype)


class HeUniform(BaseObject, init_ops.Initializer):
    CONFIG = initializations.HeUniformInitializerConfig

    def __init__(self, seed=None):
        self.seed = seed

    def __call__(self, shape, dtype=None, partition_info=None):
        return initializers.he_uniform(seed=self.seed)(shape, dtype)


class HeNormal(BaseObject, init_ops.Initializer):
    CONFIG = initializations.HeNormalInitializerConfig

    def __init__(self, seed=None):
        self.seed = seed

    def __call__(self, shape, dtype=None, partition_info=None):
        return initializers.he_normal(seed=self.seed)(shape, dtype)


class LecunUniform(BaseObject, init_ops.Initializer):
    CONFIG = initializations.LecunUniformInitializerConfig

    def __init__(self, seed=None):
        self.seed = seed

    def __call__(self, shape, dtype=None, partition_info=None):
        return initializers.lecun_uniform(seed=self.seed)(shape, dtype)


class LecunNormal(BaseObject, init_ops.Initializer):
    CONFIG = initializations.LecunNormalInitializerConfig

    def __init__(self, seed=None):
        self.seed = seed

    def __call__(self, shape, dtype=None, partition_info=None):
        return initializers.lecun_normal(seed=self.seed)(shape, dtype)


zeros = Zeros
ones = Ones
constant = Constant
uniform = Uniform
normal = Normal
truncated_normal = TruncatedNormal
variance_scaling = VarianceScaling
identity = Identity
orthogonal = Orthogonal
glorot_uniform = GlorotUniform
glorot_normal = GlorotNormal
he_uniform = HeUniform
he_normal = HeNormal
lecun_uniform = LecunUniform
lecun_normal = LecunNormal

INITIALIZERS = {
    initializations.ZerosInitializerConfig.IDENTIFIER: zeros,
    initializations.OnesInitializerConfig.IDENTIFIER: ones,
    initializations.ConstantInitializerConfig.IDENTIFIER: constant,
    initializations.UniformInitializerConfig.IDENTIFIER: uniform,
    initializations.NormalInitializerConfig.IDENTIFIER: normal,
    initializations.TruncatedNormalInitializerConfig.IDENTIFIER: truncated_normal,
    initializations.VarianceScalingInitializerConfig.IDENTIFIER: variance_scaling,
    initializations.IdentityInitializerConfig.IDENTIFIER: identity,
    initializations.OrthogonalInitializerConfig.IDENTIFIER: orthogonal,
    initializations.GlorotUniformInitializerConfig.IDENTIFIER: glorot_uniform,
    initializations.GlorotNormalInitializerConfig.IDENTIFIER: glorot_normal,
    initializations.HeUniformInitializerConfig.IDENTIFIER: he_uniform,
    initializations.HeNormalInitializerConfig.IDENTIFIER: he_normal,
    initializations.LecunNormalInitializerConfig.IDENTIFIER: lecun_normal,
    initializations.LecunUniformInitializerConfig.IDENTIFIER: lecun_uniform,
}
