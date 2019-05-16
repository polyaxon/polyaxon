# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class ExperimentFramework(object):
    TENSORFLOW = 'tensorflow'
    MXNET = 'mxnet'
    HOROVOD = 'horovod'
    PYTORCH = 'pytorch'

    VALUES = [TENSORFLOW, MXNET, HOROVOD, PYTORCH]
