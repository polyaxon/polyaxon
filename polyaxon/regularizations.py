# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras.regularizers import l1, l2, l1_l2

from polyaxon_schemas import regularizations

l1 = l1
l2 = l2
l1_l2 = l1_l2

REGULARIZERS = OrderedDict([
    (regularizations.L1RegularizerConfig.IDENTIFIER, l1),
    (regularizations.L2RegularizerConfig.IDENTIFIER, l2),
    (regularizations.L1L2RegularizerConfig.IDENTIFIER, l1_l2),
])
