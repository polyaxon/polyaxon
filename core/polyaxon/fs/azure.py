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
from adlfs import AzureBlobFileSystem as BaseAzureBlobFileSystem

from polyaxon.connections.azure.base import (
    get_account_key,
    get_account_name,
    get_client_id,
    get_client_secret,
    get_connection_string,
    get_sas_token,
    get_tenant_id,
)


class AzureBlobFileSystem(BaseAzureBlobFileSystem):
    async def _put_file(self, lpath, rpath, delimiter="/", overwrite=True, **kwargws):
        return await super()._put_file(
            lpath, rpath, delimiter=delimiter, overwrite=overwrite, **kwargws
        )

    async def _ls(
        self,
        path: str,
        force: bool = False,
        delimiter: str = "/",
        return_glob: bool = False,
        **kwargs,
    ):
        invalidate_cache = kwargs.pop("invalidate_cache", force)
        return await super()._ls(
            path,
            invalidate_cache=invalidate_cache,
            delimiter=delimiter,
            return_glob=return_glob,
            **kwargs,
        )


def get_fs(
    context_path: str = None,
    asynchronous: bool = False,
    use_listings_cache: bool = False,
    **kwargs,
):

    return AzureBlobFileSystem(
        account_name=get_account_name(context_path=context_path, **kwargs),
        account_key=get_account_key(context_path=context_path, **kwargs),
        connection_string=get_connection_string(
            context_path=context_path,
            **kwargs,
        ),
        sas_token=get_sas_token(
            context_path=context_path,
            **kwargs,
        ),
        tenant_id=get_tenant_id(
            context_path=context_path,
            **kwargs,
        ),
        client_id=get_client_id(
            context_path=context_path,
            **kwargs,
        ),
        client_secret=get_client_secret(
            context_path=context_path,
            **kwargs,
        ),
        request_session=kwargs.get("request_session"),
        asynchronous=asynchronous,
        use_listings_cache=use_listings_cache,
    )
