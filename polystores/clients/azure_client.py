# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from azure.storage.blob import BlockBlobService

from polystores.utils import get_from_env


def get_account_name(keys=None):
    keys = keys or ['AZURE_ACCOUNT_NAME']
    return get_from_env(keys)


def get_account_key(keys=None):
    keys = keys or ['AZURE_ACCOUNT_KEY']
    return get_from_env(keys)


def get_connection_string(keys=None):
    keys = keys or ['AZURE_CONNECTION_STRING']
    return get_from_env(keys)


def get_blob_service_connection(account_name=None, account_key=None, connection_string=None):
    account_name = account_name or get_account_name()
    account_key = account_key or get_account_key()
    connection_string = connection_string or get_connection_string()
    return BlockBlobService(account_name=account_name,
                            account_key=account_key,
                            connection_string=connection_string)
