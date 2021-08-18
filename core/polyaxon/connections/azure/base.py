#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

import logging

from typing import List, Optional, Union

from polyaxon.connections.reader import read_keys

logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.storage").setLevel(logging.WARNING)
logging.getLogger("azure.storage.blob").setLevel(logging.WARNING)


def get_account_name(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    # Check kwargs
    value = kwargs.get("account_name") or kwargs.get("AZURE_ACCOUNT_NAME")
    if value:
        return value
    # Check env/path keys
    keys = keys or ["AZURE_ACCOUNT_NAME"]
    return read_keys(context_path=context_path, keys=keys)


def get_account_key(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    value = kwargs.get("account_key") or kwargs.get("AZURE_ACCOUNT_KEY")
    if value:
        return value
    keys = keys or ["AZURE_ACCOUNT_KEY"]
    return read_keys(context_path=context_path, keys=keys)


def get_connection_string(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    value = kwargs.get("connection_string") or kwargs.get("AZURE_CONNECTION_STRING")
    if value:
        return value
    keys = keys or ["AZURE_CONNECTION_STRING"]
    return read_keys(context_path=context_path, keys=keys)


def get_sas_token(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    value = (
        kwargs.get("sas_token")
        or kwargs.get("AZURE_SAS_TOKEN")
        or kwargs.get("AZURE_STORAGE_SAS_TOKEN")
    )
    if value:
        return value
    keys = keys or ["AZURE_SAS_TOKEN", "AZURE_STORAGE_SAS_TOKEN"]
    return read_keys(context_path=context_path, keys=keys)


def get_tenant_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    value = kwargs.get("tenant_id") or kwargs.get("AZURE_TENANT_ID")
    if value:
        return value
    keys = keys or ["AZURE_TENANT_ID"]
    return read_keys(context_path=context_path, keys=keys)


def get_client_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    value = kwargs.get("client_id") or kwargs.get("AZURE_CLIENT_ID")
    if value:
        return value
    keys = keys or ["AZURE_CLIENT_ID"]
    return read_keys(context_path=context_path, keys=keys)


def get_client_secret(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
):
    value = kwargs.get("client_secret") or kwargs.get("AZURE_CLIENT_SECRET")
    if value:
        return value
    keys = keys or ["AZURE_CLIENT_SECRET"]
    return read_keys(context_path=context_path, keys=keys)
