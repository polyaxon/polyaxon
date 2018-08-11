# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_stores.utils import get_from_env
from polyaxon_stores.exceptions import PolyaxonStoresException
from polyaxon_stores.stores.base_store import Store


def get_outputs_path(keys=None):
    keys = keys or ['POLYAXON_RUN_OUTPUTS_PATH']
    return get_from_env(keys)


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

        self._outputs_path = outputs_path or get_outputs_path()

    @property
    def store(self):
        return self._store

    @property
    def outputs_path(self):
        return self._outputs_path

    def get_outputs_file_path(self, filename):
        return os.path.join(self.outputs_path, filename)

    def get_outputs_directory_path(self, dirname):
        return os.path.join(self.outputs_path, dirname)
