#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

from collections import Mapping
from typing import List, Optional, Union

import google.auth
import google.oauth2.service_account

from google.cloud.storage.client import Client
from google.oauth2.service_account import Credentials

from polyaxon.connections.base import BaseService
from polyaxon.connections.reader import get_connection_context_path, read_keys
from polyaxon.containers.contexts import CONTEXT_MOUNT_GC
from polyaxon.exceptions import PolyaxonStoresException
from polyaxon.logger import logger
from polyaxon.utils.path_utils import create_polyaxon_tmp

DEFAULT_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)


def get_project_id(
    keys: Optional[Union[str, List[str]]] = None, context_path: Optional[str] = None
):
    keys = keys or [
        "GC_PROJECT",
        "GOOGLE_PROJECT",
        "GC_PROJECT_ID",
        "GOOGLE_PROJECT_ID",
    ]
    return read_keys(context_path=context_path, keys=keys)


def get_key_path(
    keys: Optional[Union[str, List[str]]] = None, context_path: Optional[str] = None
):
    keys = keys or ["GC_KEY_PATH", "GOOGLE_KEY_PATH", "GOOGLE_APPLICATION_CREDENTIALS"]
    return read_keys(context_path=context_path, keys=keys)


def get_keyfile_dict(
    keys: Optional[Union[str, List[str]]] = None, context_path: Optional[str] = None
):
    keys = keys or ["GC_KEYFILE_DICT", "GOOGLE_KEYFILE_DICT"]
    return read_keys(context_path=context_path, keys=keys)


def get_scopes(
    keys: Optional[Union[str, List[str]]] = None, context_path: Optional[str] = None
):
    keys = keys or ["GC_SCOPES", "GOOGLE_SCOPES"]
    return read_keys(context_path=context_path, keys=keys)


def get_gc_credentials(
    key_path=None, keyfile_dict=None, scopes=None, context_path: Optional[str] = None
):
    """
    Returns the Credentials object for Google API
    """
    key_path = key_path or get_key_path(context_path=context_path)
    keyfile_dict = keyfile_dict or get_keyfile_dict(context_path=context_path)
    scopes = scopes or get_scopes(context_path=context_path)

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
    key_path=None,
    keyfile_dict=None,
    credentials=None,
    scopes=None,
    context_path: Optional[str] = None,
):
    credentials = credentials or get_gc_credentials(
        key_path=key_path,
        keyfile_dict=keyfile_dict,
        scopes=scopes,
        context_path=context_path,
    )
    return credentials.token


def get_gc_client(
    project_id=None,
    key_path=None,
    keyfile_dict=None,
    credentials=None,
    scopes=None,
    context_path: Optional[str] = None,
):
    credentials = credentials or get_gc_credentials(
        key_path=key_path,
        keyfile_dict=keyfile_dict,
        scopes=scopes,
        context_path=context_path,
    )
    project_id = project_id or get_project_id()
    return Client(project=project_id, credentials=credentials)


class GCPService(BaseService):
    def __init__(self, connection=None, **kwargs):
        super().__init__(connection=connection, **kwargs)
        self._project_id = kwargs.get("project_id")
        self._credentials = kwargs.get("credentials")
        self._key_path = kwargs.get("key_path")
        self._keyfile_dict = kwargs.get("keyfile_dict")
        self._scopes = kwargs.get("scopes")
        self._encoding = kwargs.get("encoding", "utf-8")

    def set_connection(
        self,
        connection=None,
        connection_type=None,
        project_id=None,
        key_path=None,
        keyfile_dict=None,
        credentials=None,
        scopes=None,
    ):
        """
        Sets a new gc client.

        Args:
            project_id: `str`. The project if.
            key_path: `str`. The path to the json key file.
            keyfile_dict: `str`. The dict containing the auth data.
            credentials: `Credentials instance`. The credentials to use.
            scopes: `list`. The scopes.

        Returns:
            Service client instance
        """
        if connection:
            self._connection = connection
            return
        connection_type = connection_type or self._connection_type
        connection_name = connection_type.name if connection_type else None
        context_path = get_connection_context_path(name=connection_name)
        self._connection = get_gc_client(
            project_id=project_id or self._project_id,
            key_path=key_path or self._key_path,
            keyfile_dict=keyfile_dict or self._keyfile_dict,
            credentials=credentials or self._credentials,
            scopes=scopes or self._scopes,
            context_path=context_path,
        )

    def set_env_vars(self):
        if self._key_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self._key_path
        elif self._keyfile_dict:
            create_polyaxon_tmp()
            with open(CONTEXT_MOUNT_GC, "w") as outfile:
                json.dump(self._keyfile_dict, outfile)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CONTEXT_MOUNT_GC
