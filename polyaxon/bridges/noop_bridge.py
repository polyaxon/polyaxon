# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


from polyaxon import Modes
from polyaxon.bridges.base import BaseBridge, BridgeSpec


class NoOpBridge(BaseBridge):
    """A bridge that passes the encoder output to the decoder.

    Args:
        mode: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
        name: `str`. The name of this bridge, used for creating the scope.
        state_size: `int`. The bridge state size. Default None, it will be inferred
        directly from the incoming tensor.
    """
    def __init__(self, mode, state_size=None, name="NoOpBridge"):
        super(NoOpBridge, self).__init__(mode=mode, state_size=state_size, name=name)

    def _build(self, features, labels, loss, encoder_fn, decoder_fn, *args, **kwargs):
        losses, loss = None, None
        if Modes.GENERATE == self.mode:
            results = self.decode(
                incoming=features, features=features, labels=labels, decoder_fn=decoder_fn)
        elif Modes.ENCODE == self.mode:
            results = self.encode(features=features, labels=labels, encoder_fn=encoder_fn)
        else:
            x = self.encode(features=features, labels=labels, encoder_fn=encoder_fn)
            results = self.decode(features=x, labels=labels, decoder_fn=decoder_fn)
            if not Modes.is_infer(self.mode):
                losses, loss = self._build_loss(results, features, labels, loss)

        return BridgeSpec(results=results, losses=losses, loss=loss)
