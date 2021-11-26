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

from polyaxon.connections.base import BaseService
from polyaxon.connections.gcp.base import get_gc_client
from polyaxon.connections.reader import get_connection_context_path
from polyaxon.containers.contexts import CONTEXT_MOUNT_GC
from polyaxon.utils.path_utils import create_polyaxon_tmp

DEFAULT_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)


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
