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


class Multiply(BaseObject, merge.Multiply):
    CONFIG = MultiplyConfig


class Average(BaseObject, merge.Average):
    CONFIG = AverageConfig


class Maximum(BaseObject, merge.Maximum):
    CONFIG = MaximumConfig


class Concatenate(BaseObject, merge.Concatenate):
    CONFIG = ConcatenateConfig


class Dot(BaseObject, merge.Dot):
    CONFIG = DotConfig


MERGE_LAYERS = OrderedDict([
    (Add.CONFIG.IDENTIFIER, Add),
    # ('Subtract', Subtract),
    (Multiply.CONFIG.IDENTIFIER, Multiply),
    (Average.CONFIG.IDENTIFIER, Average),
    (Maximum.CONFIG.IDENTIFIER, Maximum),
    (Concatenate.CONFIG.IDENTIFIER, Concatenate),
    (Dot.CONFIG.IDENTIFIER, Dot),
])
