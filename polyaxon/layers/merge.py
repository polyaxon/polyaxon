from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.layers import merge

from polyaxon.libs.base_object import BaseObject
from polyaxon_schemas.layers.merge import (
    AddConfig,
    MultiplyConfig,
    AverageConfig,
    MaximumConfig,
    ConcatenateConfig,
    DotConfig,
)


class Add(BaseObject, merge.Add):
    CONFIG = AddConfig
    __doc__ = merge.Add.__doc__


class Multiply(BaseObject, merge.Multiply):
    CONFIG = MultiplyConfig
    __doc__ = merge.Multiply.__doc__


class Average(BaseObject, merge.Average):
    CONFIG = AverageConfig
    __doc__ = merge.Average.__doc__


class Maximum(BaseObject, merge.Maximum):
    CONFIG = MaximumConfig
    __doc__ = merge.Maximum.__doc__


class Concatenate(BaseObject, merge.Concatenate):
    CONFIG = ConcatenateConfig
    __doc__ = merge.Concatenate.__doc__


class Dot(BaseObject, merge.Dot):
    CONFIG = DotConfig
    __doc__ = merge.Dot.__doc__


MERGE_LAYERS = OrderedDict([
    (Add.CONFIG.IDENTIFIER, Add),
    # ('Subtract', Subtract),  # TODO: Add when upgrading to tensorflow 1.4.0
    (Multiply.CONFIG.IDENTIFIER, Multiply),
    (Average.CONFIG.IDENTIFIER, Average),
    (Maximum.CONFIG.IDENTIFIER, Maximum),
    (Concatenate.CONFIG.IDENTIFIER, Concatenate),
    (Dot.CONFIG.IDENTIFIER, Dot),
])
