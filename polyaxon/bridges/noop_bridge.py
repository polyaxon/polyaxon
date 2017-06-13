# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.bridges.base import BaseBridge, BridgeSpec


class NoOpBridge(BaseBridge):
    """A bridge that passes the encoder to the decoder outputs.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
        name: `str`. The name of this bridge, used for creating the scope.
        state_size: `int`. The bridge state size. Default None, it will be inferred
        directly from the incoming tensor.
    """
    def __init__(self, mode, state_size=None, name="NoOpBridge"):
        super(NoOpBridge, self).__init__(mode=mode, state_size=state_size, name=name)

    def _build(self, incoming, encoder_fn, decoder_fn, *args, **kwargs):
        x = self.encode(incoming=incoming, encoder_fn=encoder_fn)
        results = self.decode(incoming=x, decoder_fn=decoder_fn)
        return BridgeSpec(encoded=x,
                          generated=self.decode(incoming=incoming, decoder_fn=decoder_fn),
                          results=results,
                          losses=None,
                          loss=None)
