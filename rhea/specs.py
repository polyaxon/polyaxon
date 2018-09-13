# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import namedtuple


class UriSpec(namedtuple("UriSpec", "user password host")):
    """
    A specification for uris configuration.
    """
    pass
