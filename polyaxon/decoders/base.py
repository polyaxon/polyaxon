# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
from collections import namedtuple

import six

from polyaxon.libs.subgraph import SubGraph
from polyaxon.libs.utils import get_shape

DecoderSpec = namedtuple("DecoderSpec", "output output_size")


@six.add_metaclass(abc.ABCMeta)
class Decoder(SubGraph):
    """An abstract base class for defining a decoder.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`. The name of this bridge, used for creating the scope.
    """
    def __init__(self, mode, modules, name="Decoder", features=None):
        super(Decoder, self).__init__(mode=mode, modules=modules, name=name, features=features)

    def _build(self, incoming, *args, **kwargs):
        """Creates the encoder logic and returns an `DecoderSpec`."""
        incoming = self.decode(incoming, *args, **kwargs)
        return DecoderSpec(output=incoming,
                           output_size=self.output_size(incoming))

    def decode(self, incoming, *args, **kwargs):
        """Subclasses should implement their logic here."""
        return super(Decoder, self)._build(incoming, *args, **kwargs)

    def generate(self, distribution):
        pass

    def output_size(self, incoming):
        return get_shape(incoming)[1:]
