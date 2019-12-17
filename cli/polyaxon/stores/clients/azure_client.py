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

from azure.storage.blob import BlockBlobService

from polyaxon.stores.utils import get_from_env


def get_account_name(keys=None):
    keys = keys or ["AZURE_ACCOUNT_NAME"]
    return get_from_env(keys)


def get_account_key(keys=None):
    keys = keys or ["AZURE_ACCOUNT_KEY"]
    return get_from_env(keys)


def get_connection_string(keys=None):
    keys = keys or ["AZURE_CONNECTION_STRING"]
    return get_from_env(keys)


def get_blob_service_connection(
    account_name=None, account_key=None, connection_string=None
):
    account_name = account_name or get_account_name()
    account_key = account_key or get_account_key()
    connection_string = connection_string or get_connection_string()
    return BlockBlobService(
        account_name=account_name,
        account_key=account_key,
        connection_string=connection_string,
    )
