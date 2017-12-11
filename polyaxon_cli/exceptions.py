# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from click import ClickException


class PolyaxonException(ClickException):
    def __init__(self, message=None):
        super(PolyaxonException, self).__init__(message)


class PolyaxonConfigurationError(PolyaxonException):
    """Exception class to raise if a Configurable object has an issue."""
    pass
