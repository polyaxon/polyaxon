# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

from tensorflow.contrib.keras.python.keras import regularizers

from polyaxon_schemas import regularizations

from polyaxon.libs.base_object import BaseObject


class L1L2(BaseObject, regularizers.L1L2):
    CONFIG = regularizations.L1L2RegularizerConfig
    __doc__ = regularizers.L1L2.__doc__


class L1(BaseObject, regularizers.L1L2):
    """Regularizer for L1 regularization.

     Arguments:
         l: Float; regularization factor.
     """

    CONFIG = regularizations.L1RegularizerConfig

    def __init__(self, l=0.):
        super(L1, self).__init__(l1=l)


class L2(BaseObject, regularizers.L1L2):
    """Regularizer for L2 regularization.

     Arguments:
         l: Float; regularization factor.
     """

    CONFIG = regularizations.L2RegularizerConfig

    def __init__(self, l=0.):
        super(L2, self).__init__(l2=l)


def l1(l=0.01):
    return L1(l=l)

l1.__doc__ = L1.__doc__


def l2(l=0.01):
    return L2(l=l)

l2.__doc__ = L2.__doc__


def l1_l2(l1=0.01, l2=0.01):
    return L1L2(l1=l1, l2=l2)


l1_l2.__doc__ = L1L2.__doc__


REGULARIZERS = OrderedDict([
    (regularizations.L1RegularizerConfig.IDENTIFIER, l1),
    (regularizations.L2RegularizerConfig.IDENTIFIER, l2),
    (regularizations.L1L2RegularizerConfig.IDENTIFIER, l1_l2),
])
