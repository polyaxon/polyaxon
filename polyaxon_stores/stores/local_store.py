# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


from polyaxon_stores.stores.base_store import Store


class LocalStore(Store):
    """
    Local filesystem store.

    This store is noop store since all data is accessible through the filesystem.
    """
    STORE_TYPE = Store._LOCAL_STORE  # pylint:disable=protected-access

    def download_file(self, *args, **kwargs):
        pass

    def upload_file(self, *args, **kwargs):
        pass

    def upload_files(self, dirname, path=None):
        pass

    def download_files(self, *args, **kwargs):
        pass

