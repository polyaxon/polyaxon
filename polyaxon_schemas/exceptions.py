# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class PolyaxonSchemaError(Exception):
    """Exception class to raise if a schema has an issue."""
    pass


class PolyaxonfileError(Exception):
    """Exception class to raise if an error is encountered during the parsing of a Polyaxonfile."""
    pass


class PolyaxonConfigurationError(Exception):
    """Exception class to raise if a Configurable object has an issue."""
    pass
