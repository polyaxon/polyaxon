# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.stores.exceptions import PolyaxonStoresException
from polyaxon_client.stores.stores.base_store import Store


class OutputsStore(object):
    """
    A convenient class to store experiment/job outputs to a given/configured store.
    """

    def __init__(self, store=None, outputs_path=None):
        store = store or Store.get_store()
        if isinstance(store, Store):
            self._store = store
        else:
            raise PolyaxonStoresException('Received an unrecognised store `{}`.'.format(store))

        self._outputs_path = outputs_path

    def set_store(self, store):
        self._store = store

    def set_outputs_path(self, outputs_path):
        self._outputs_path = outputs_path

    @property
    def store(self):
        return self._store

    @property
    def outputs_path(self):
        return self._outputs_path

    def upload_file(self, filename, **kwargs):
        self.store.upload_file(filename, self.outputs_path, **kwargs)

    def upload_dir(self, dirname, **kwargs):
        self.store.upload_dir(dirname, self.outputs_path, **kwargs)
