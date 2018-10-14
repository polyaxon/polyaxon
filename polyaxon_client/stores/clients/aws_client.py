# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import boto3

from polyaxon_client.stores.utils import get_from_env


def get_aws_access_key_id(keys=None):
    keys = keys or ['AWS_ACCESS_KEY_ID']
    return get_from_env(keys)


def get_aws_secret_access_key(keys=None):
    keys = keys or ['AWS_SECRET_ACCESS_KEY']
    return get_from_env(keys)


def get_aws_security_token(keys=None):
    keys = keys or ['AWS_SECURITY_TOKEN']
    return get_from_env(keys)


def get_region(keys=None):
    keys = keys or ['AWS_REGION']
    return get_from_env(keys)


def get_endpoint_url(keys=None):
    keys = keys or ['AWS_ENDPOINT_URL']
    return get_from_env(keys)


def get_aws_session(aws_access_key_id=None,
                    aws_secret_access_key=None,
                    aws_session_token=None,
                    region_name=None):
    aws_access_key_id = aws_access_key_id or get_aws_access_key_id()
    aws_secret_access_key = aws_secret_access_key or get_aws_secret_access_key()
    aws_session_token = aws_session_token or get_aws_security_token()
    region_name = region_name or get_region()
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name)


def get_aws_client(client_type,
                   endpoint_url=None,
                   aws_access_key_id=None,
                   aws_secret_access_key=None,
                   aws_session_token=None,
                   region_name=None):
    session = get_aws_session(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token,
                              region_name=region_name)
    endpoint_url = endpoint_url or get_endpoint_url()
    return session.client(client_type, endpoint_url=endpoint_url)


def get_aws_resource(resource_type,
                     endpoint_url=None,
                     aws_access_key_id=None,
                     aws_secret_access_key=None,
                     aws_session_token=None,
                     region_name=None):
    session = get_aws_session(aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token,
                              region_name=region_name)
    endpoint_url = endpoint_url or get_endpoint_url()
    return session.resource(resource_type, endpoint_url=endpoint_url)
