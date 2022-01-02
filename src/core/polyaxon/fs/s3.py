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
from s3fs import S3FileSystem as BaseS3FileSystem

from polyaxon.connections.aws.base import (
    get_aws_access_key_id,
    get_aws_secret_access_key,
    get_aws_security_token,
    get_aws_use_ssl,
    get_aws_verify_ssl,
    get_endpoint_url,
    get_region,
)


class S3FileSystem(BaseS3FileSystem):
    async def _ls(self, path, detail=False, force=False):
        return await super()._ls(path, detail=detail, refresh=force)


def get_fs(
    context_path: str = None,
    asynchronous: bool = False,
    use_listings_cache: bool = False,
    **kwargs
):

    config_kwargs = {}
    region_name = get_region(context_path=context_path, **kwargs)
    if region_name:
        config_kwargs["region_name"] = region_name

    client_kwargs = {}
    endpoint_url = get_endpoint_url(context_path=context_path, **kwargs)
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url
    verify_ssl = get_aws_verify_ssl(context_path=context_path, **kwargs)
    if verify_ssl is not None:
        client_kwargs["verify"] = verify_ssl

    return S3FileSystem(
        key=get_aws_access_key_id(context_path=context_path, **kwargs),
        secret=get_aws_secret_access_key(context_path=context_path, **kwargs),
        token=get_aws_security_token(context_path=context_path, **kwargs),
        use_ssl=get_aws_use_ssl(context_path=context_path, **kwargs),
        config_kwargs=config_kwargs,
        client_kwargs=client_kwargs,
        session=kwargs.get("session"),
        asynchronous=asynchronous,
        use_listings_cache=use_listings_cache,
    )
