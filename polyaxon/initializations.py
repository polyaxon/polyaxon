# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


from tensorflow.contrib.keras.python.keras.initializers import (
    Identity,
    he_uniform,
    he_normal,
    lecun_normal,
    lecun_uniform,
    glorot_normal,
    glorot_uniform,
)
from tensorflow.python.ops import init_ops

from polyaxon_schemas import initializations


zeros = init_ops.Zeros
ones = init_ops.Ones
constant = init_ops.Constant
uniform = init_ops.RandomUniform
normal = init_ops.RandomNormal
truncated_normal = init_ops.TruncatedNormal
variance_scaling = init_ops.VarianceScaling
identity = Identity
orthogonal = init_ops.Orthogonal
glorot_uniform = glorot_uniform
glorot_normal = glorot_normal
he_uniform = he_uniform
he_normal = he_normal
lecun_normal = lecun_normal
lecun_uniform = lecun_uniform


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
