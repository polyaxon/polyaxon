# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from polyaxon.bridges.base import BridgeSpec, BaseBridge
from polyaxon.bridges.latent_bridge import LatentBridge
from polyaxon.bridges.noop_bridge import NoOpBridge

BRIDGES = OrderedDict([
    ('NoOpBridge', NoOpBridge),
    ('LatentBridge', LatentBridge),
])
