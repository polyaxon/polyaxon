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

from typing import List, Optional, Union

from polyaxon.connections.reader import read_keys


def get_aws_access_key_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("access_key_id")
        or kwargs.get("aws_access_key_id")
        or kwargs.get("AWS_ACCESS_KEY_ID")
    )
    if value:
        return value
    keys = keys or ["AWS_ACCESS_KEY_ID"]
    return read_keys(context_path=context_path, keys=keys)


def get_aws_secret_access_key(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("secret_access_key")
        or kwargs.get("aws_secret_access_key")
        or kwargs.get("AWS_SECRET_ACCESS_KEY")
    )
    if value:
        return value
    keys = keys or ["AWS_SECRET_ACCESS_KEY"]
    return read_keys(context_path=context_path, keys=keys)


def get_aws_security_token(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("session_token")
        or kwargs.get("aws_session_token")
        or kwargs.get("security_token")
        or kwargs.get("aws_security_token")
        or kwargs.get("AWS_SECURITY_TOKEN")
    )
    if value:
        return value
    keys = keys or ["AWS_SECURITY_TOKEN"]
    return read_keys(context_path=context_path, keys=keys)


def get_region(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("region")
        or kwargs.get("region_name")
        or kwargs.get("aws_region")
        or kwargs.get("AWS_REGION")
    )
    if value:
        return value
    keys = keys or ["AWS_REGION"]
    return read_keys(context_path=context_path, keys=keys)


def get_endpoint_url(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("endpoint_url")
        or kwargs.get("aws_endpoint_url")
        or kwargs.get("AWS_ENDPOINT_URL")
    )
    if value:
        return value
    keys = keys or ["AWS_ENDPOINT_URL"]
    return read_keys(context_path=context_path, keys=keys)


def get_aws_use_ssl(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("use_ssl") or kwargs.get("aws_use_ssl") or kwargs.get("AWS_USE_SSL")
    )
    if value is not None:
        return value
    keys = keys or ["AWS_USE_SSL"]
    value = read_keys(context_path=context_path, keys=keys)
    if value is not None:
        return value
    return True


def get_aws_verify_ssl(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = kwargs.get(
        "verify_ssl",
        kwargs.get("aws_verify_ssl", kwargs.get("AWS_VERIFY_SSL", None)),
    )
    if value is not None:
        return value
    keys = keys or ["AWS_VERIFY_SSL"]
    value = read_keys(context_path=context_path, keys=keys)
    if value is not None:
        return value
    return True


def get_aws_legacy_api(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
):
    value = (
        kwargs.get("legacy_api")
        or kwargs.get("aws_legacy_api")
        or kwargs.get("AWS_LEGACY_API")
    )
    if value:
        return value
    keys = keys or ["AWS_LEGACY_API"]
    return read_keys(context_path=context_path, keys=keys)


def get_legacy_api(legacy_api=False, **kwargs):
    legacy_api = legacy_api or get_aws_legacy_api(**kwargs)
    return legacy_api


def get_aws_session(
    context_path=None,
    **kwargs,
):
    import boto3

    aws_access_key_id = get_aws_access_key_id(context_path=context_path, **kwargs)
    aws_secret_access_key = get_aws_secret_access_key(
        context_path=context_path, **kwargs
    )
    aws_session_token = get_aws_security_token(context_path=context_path, **kwargs)
    region_name = get_region(context_path=context_path, **kwargs)
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )


def get_aws_client(
    client_type,
    context_path=None,
    **kwargs,
):
    session = get_aws_session(
        context_path=context_path,
        **kwargs,
    )
    endpoint_url = get_endpoint_url(context_path=context_path, **kwargs)
    aws_use_ssl = get_aws_use_ssl(context_path=context_path, **kwargs)
    aws_verify_ssl = get_aws_verify_ssl(context_path=context_path, **kwargs)
    return session.client(
        client_type,
        endpoint_url=endpoint_url,
        use_ssl=aws_use_ssl,
        verify=aws_verify_ssl,
    )


def get_aws_resource(
    resource_type,
    context_path=None,
    **kwargs,
):
    session = get_aws_session(
        context_path=context_path,
        **kwargs,
    )
    endpoint_url = get_endpoint_url(context_path=context_path, **kwargs)
    aws_use_ssl = get_aws_use_ssl(context_path=context_path, **kwargs)
    aws_verify_ssl = get_aws_verify_ssl(context_path=context_path, **kwargs)
    return session.resource(
        resource_type,
        endpoint_url=endpoint_url,
        use_ssl=aws_use_ssl,
        verify=aws_verify_ssl,
    )
