# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.stores.stores.base_store import BaseStore


class LocalStore(BaseStore):
    """
    Local filesystem store.

    This store is noop store since all data is accessible through the filesystem.
    """
    # pylint:disable=arguments-differ

    STORE_TYPE = BaseStore._LOCAL_STORE  # pylint:disable=protected-access

    def download_file(self, *args, **kwargs):
        pass

    def upload_file(self, *args, **kwargs):
        pass

    def upload_dir(self, *args, **kwargs):
        pass

    def download_dir(self, *args, **kwargs):
        pass
