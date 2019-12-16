# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from azure.storage.blob import BlockBlobService

from polystores.clients.azure_client import get_blob_service_connection


class TestAzureClient(TestCase):
    def test_get_blob_service_connection(self):
        with self.assertRaises(ValueError):
            get_blob_service_connection()

        service = get_blob_service_connection(account_name='foo', account_key='bar')
        assert isinstance(service, BlockBlobService)

        os.environ['AZURE_ACCOUNT_NAME'] = 'foo'
        os.environ['AZURE_ACCOUNT_KEY'] = 'bar'
        service = get_blob_service_connection()
        assert isinstance(service, BlockBlobService)
