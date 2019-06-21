# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import namedtuple


class UriSpec(namedtuple("UriSpec", "user password host")):
    """
    A specification for uris configuration.
    """
    pass


class AuthSpec(namedtuple("UriSpec", "user password")):
    """
    A specification for auth configuration.
    """
    pass


class WasbsSpec(namedtuple("WasbsSpec", "container storage_account path")):
    """
    A specification for wasbs configuration.
    """


class GCSSpec(namedtuple("GCSSpec", "bucket blob")):
    """
    A specification for gcs configuration.
    """


class S3Spec(namedtuple("S3Spec", "bucket key")):
    """
    A specification for s3 configuration.
    """
