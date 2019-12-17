#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8
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
