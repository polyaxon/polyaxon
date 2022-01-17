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

import json
import os

from collections.abc import Mapping
from typing import List, Optional, Union

import google.auth
import google.oauth2.service_account

from google.oauth2.service_account import Credentials

from polyaxon.connections.reader import read_keys
from polyaxon.containers.contexts import CONTEXT_MOUNT_GC
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.logger import logger

DEFAULT_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)


def get_project_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = kwargs.get("project_id")
    if value:
        return value
    keys = keys or [
        "GC_PROJECT",
        "GOOGLE_PROJECT",
        "GC_PROJECT_ID",
        "GOOGLE_PROJECT_ID",
    ]
    return read_keys(context_path=context_path, keys=keys)


def get_key_path(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = kwargs.get("key_path")
    if value:
        return value
    keys = keys or ["GC_KEY_PATH", "GOOGLE_KEY_PATH", "GOOGLE_APPLICATION_CREDENTIALS"]
    return read_keys(context_path=context_path, keys=keys)


def get_keyfile_dict(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = kwargs.get("keyfile_dict")
    if value:
        return value
    keys = keys or ["GC_KEYFILE_DICT", "GOOGLE_KEYFILE_DICT"]
    return read_keys(context_path=context_path, keys=keys)


def get_scopes(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = kwargs.get("scopes")
    if value:
        return value
    keys = keys or ["GC_SCOPES", "GOOGLE_SCOPES"]
    return read_keys(context_path=context_path, keys=keys)


def get_gc_credentials(
    context_path: Optional[str] = None,
    **kwargs,
):
    """
    Returns the Credentials object for Google API
    """
    key_path = get_key_path(context_path=context_path, **kwargs)
    keyfile_dict = get_keyfile_dict(context_path=context_path, **kwargs)
    scopes = get_scopes(context_path=context_path, **kwargs)

    if scopes is not None:
        scopes = [s.strip() for s in scopes.split(",")]
    else:
        scopes = DEFAULT_SCOPES

    if not key_path and not keyfile_dict:
        # Look for default GC path
        if os.path.exists(CONTEXT_MOUNT_GC):
            key_path = CONTEXT_MOUNT_GC

    if not key_path and not keyfile_dict:
        logger.info(
            "Getting connection using `google.auth.default()` "
            "since no key file is defined for hook."
        )
        credentials, _ = google.auth.default(scopes=scopes)
    elif key_path:
        # Get credentials from a JSON file.
        if key_path.endswith(".json"):
            logger.info("Getting connection using a JSON key file.")
            credentials = Credentials.from_service_account_file(
                os.path.abspath(key_path), scopes=scopes
            )
        else:
            raise PolyaxonStoresException("Unrecognised extension for key file.")
    else:
        # Get credentials from JSON data.
        try:
            if not isinstance(keyfile_dict, Mapping):
                keyfile_dict = json.loads(keyfile_dict)

            # Convert escaped newlines to actual newlines if any.
            keyfile_dict["private_key"] = keyfile_dict["private_key"].replace(
                "\\n", "\n"
            )

            credentials = Credentials.from_service_account_info(
                keyfile_dict, scopes=scopes
            )
        except ValueError:  # json.decoder.JSONDecodeError does not exist on py2
            raise PolyaxonStoresException("Invalid key JSON.")

    return credentials


def get_gc_access_token(
    credentials=None,
    context_path: Optional[str] = None,
    **kwargs,
):
    credentials = credentials or get_gc_credentials(context_path=context_path, **kwargs)
    return credentials.token


def get_gc_client(
    credentials=None,
    context_path: Optional[str] = None,
    **kwargs,
):
    from google.cloud.storage.client import Client

    credentials = credentials or get_gc_credentials(context_path=context_path, **kwargs)
    project_id = get_project_id(context_path=context_path, **kwargs)
    return Client(project=project_id, credentials=credentials)
