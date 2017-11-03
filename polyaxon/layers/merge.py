from collections import OrderedDict

try:
    from tensorflow.python.keras._impl.keras.layers import merge
    tf_14 = True
except ImportError:
    from tensorflow.contrib.keras.python.keras.layers import merge
    tf_14 = False

from polyaxon.libs.base_object import BaseObject
from polyaxon_schemas.layers.merge import (
    AddConfig,
    MultiplyConfig,
    AverageConfig,
    MaximumConfig,
    ConcatenateConfig,
    DotConfig,
    SubtractConfig)


class Add(BaseObject, merge.Add):
    CONFIG = AddConfig
    __doc__ = AddConfig.__doc__


if tf_14:
    class Subtract(BaseObject, merge.Subtract):
        CONFIG = SubtractConfig
        __doc__ = SubtractConfig.__doc__
else:
    pass


class Multiply(BaseObject, merge.Multiply):
    CONFIG = MultiplyConfig
    __doc__ = MultiplyConfig.__doc__


class Average(BaseObject, merge.Average):
    CONFIG = AverageConfig
    __doc__ = AverageConfig.__doc__


class Maximum(BaseObject, merge.Maximum):
    CONFIG = MaximumConfig
    __doc__ = MaximumConfig.__doc__


class Concatenate(BaseObject, merge.Concatenate):
    CONFIG = ConcatenateConfig
    __doc__ = ConcatenateConfig.__doc__


class Dot(BaseObject, merge.Dot):
    CONFIG = DotConfig
    __doc__ = DotConfig.__doc__


MERGE_LAYERS = OrderedDict([
    (Add.CONFIG.IDENTIFIER, Add),
    (Multiply.CONFIG.IDENTIFIER, Multiply),
    (Average.CONFIG.IDENTIFIER, Average),
    (Maximum.CONFIG.IDENTIFIER, Maximum),
    (Concatenate.CONFIG.IDENTIFIER, Concatenate),
    (Dot.CONFIG.IDENTIFIER, Dot),
])

if tf_14:
    MERGE_LAYERS[Subtract.CONFIG.IDENTIFIER] = Subtract
