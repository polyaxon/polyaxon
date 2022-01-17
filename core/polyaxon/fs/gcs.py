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
from gcsfs import GCSFileSystem as BaseGCSFileSystem

from polyaxon.connections.gcp.base import get_gc_credentials, get_project_id


class GCSFileSystem(BaseGCSFileSystem):
    retries = 3


def get_fs(
    context_path: str = None,
    asynchronous: bool = False,
    use_listings_cache: bool = False,
    **kwargs
):

    return GCSFileSystem(
        project=get_project_id(context_path=context_path, **kwargs),
        token=get_gc_credentials(context_path=context_path, **kwargs),
        asynchronous=asynchronous,
        use_listings_cache=use_listings_cache,
    )
