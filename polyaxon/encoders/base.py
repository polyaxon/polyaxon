# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
from collections import namedtuple

import six

from polyaxon.experiments import SubGraph
from polyaxon.libs.template_module import GraphModule
from polyaxon.libs.utils import get_shape

EncoderSpec = namedtuple("EncoderSpec", "output output_size")


class Encoder(SubGraph):
    """An abstract base class for defining an encoder.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`. The name of this encoder, used for creating the scope.
    """
    def __init__(self, mode, modules, name="Encoder", features=None):
        super(Encoder, self).__init__(mode=mode, modules=modules, name=name, features=features)

    def _build(self, incoming, *args, **kwargs):
        """Creates the encoder logic and returns an `EncoderSpec`."""
        incoming = self.encode(incoming, *args, **kwargs)
        return EncoderSpec(output=incoming,
                           output_size=self.output_size(incoming))

    def encode(self, incoming, *args, **kwargs):
        """Subclasses should implement their logic here."""
        return super(Encoder, self)._build(incoming, *args, **kwargs)

    def output_size(self, incoming):
        return get_shape(incoming)[1:]


