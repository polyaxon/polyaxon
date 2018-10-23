# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.stores.exceptions import PolyaxonStoresException
from polyaxon_client.stores.stores.base_store import BaseStore


class Store(object):
    """
    A convenient class to store experiment/job outputs to a given/configured store.
    """

    def __init__(self, store=None, path=None):
        self._path = path
        if not store and path:
            store = BaseStore.get_store_for_path(path=path)
        if not store:
            store = BaseStore.get_store()
        if isinstance(store, BaseStore):
            self._store = store
        else:
            raise PolyaxonStoresException('Received an unrecognised store `{}`.'.format(store))

    def set_store(self, store):
        self._store = store

    def set_path(self, path):
        self._path = path

    def set_env_vars(self):
        """Set authentication and access of the current store to the env vars"""
        if self.store:
            self.store.set_env_vars()

    @property
    def store(self):
        return self._store

    @property
    def path(self):
        return self._path

    def upload_file(self, filename, **kwargs):
        self.store.upload_file(filename, self._path, **kwargs)

    def upload_dir(self, dirname, **kwargs):
        self.store.upload_dir(dirname, self._path, **kwargs)

    def download_file(self, filename, **kwargs):
        self.store.download_file(filename, self._path, **kwargs)

    def download_dir(self, dirname, **kwargs):
        self.store.download_dir(dirname, self._path, **kwargs)
