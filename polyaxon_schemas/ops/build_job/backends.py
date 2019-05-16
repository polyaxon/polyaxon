# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class BuildBackend(object):
    NATIVE = 'native'
    KANIKO = 'kaniko'
    OTHER = 'other'

    VALUES = [NATIVE, KANIKO, OTHER]
