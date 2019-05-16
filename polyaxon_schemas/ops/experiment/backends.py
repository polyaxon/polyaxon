# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class ExperimentBackend(object):
    NATIVE = 'native'
    KUBEFLOW = 'kubeflow'
    MPI = 'mpi'
    OTHER = 'other'

    VALUES = [NATIVE, KUBEFLOW, MPI, OTHER]
