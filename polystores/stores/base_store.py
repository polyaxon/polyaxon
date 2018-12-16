# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rhea import RheaError

from polystores import settings
from polystores.exceptions import PolyaxonStoresException
from polystores.utils import get_from_env


class BaseStore(object):
    """
    A base store interface.
    """
    _LOCAL_STORE = 'local'
    _AZURE_STORE = 'azure'
    _S3_STORE = 's3'
    _GCS_STORE = 'gcs'
    _STORE_TYPES = {_LOCAL_STORE, _AZURE_STORE, _S3_STORE, _GCS_STORE}

    STORE_TYPE = None

    @classmethod
    def get_store(cls, store_type=None, **kwargs):
        store_type = store_type or get_from_env(['POLYAXON_STORE'])
        # We assume that `None` refers to local store as well
        store_type = cls._LOCAL_STORE if store_type is None else store_type
        if store_type not in cls._STORE_TYPES:
            raise PolyaxonStoresException(
                'Received an unrecognised store type `{}`.'.format(store_type))

        if store_type == cls._LOCAL_STORE:
            from polystores.stores.local_store import LocalStore
            return LocalStore()
        if store_type == cls._AZURE_STORE:
            from polystores.stores.azure_store import AzureStore
            return AzureStore(**kwargs)
        if store_type == cls._S3_STORE:
            from polystores.stores.s3_store import S3Store
            return S3Store(**kwargs)
        if store_type == cls._GCS_STORE:
            from polystores.stores.gcs_store import GCSStore
            return GCSStore(**kwargs)

        raise PolyaxonStoresException(
            'Received an unrecognised store type `{}`.'.format(store_type))

    @classmethod
    def get_store_for_path(cls, path):
        store_access = settings.RUN_STORES_ACCESS_KEYS.get(path)
        if not store_access:
            return cls.get_store()

        if 'store' not in store_access or 'secret_key' not in store_access:
            raise PolyaxonStoresException(
                'Received an invalid store access definition.')

        store_type = store_access['store']
        try:
            store_access = settings.config.get_dict(store_access['secret_key'])
        except RheaError:
            raise PolyaxonStoresException(
                'Could not create store for path `{}`,'
                'received a store type `{}` without valid access key.'.format(path, store_type))

        return cls.get_store_for_type(store_type=store_type, store_access=store_access)

    @classmethod
    def get_store_for_type(cls, store_type, store_access):
        if store_type == cls._GCS_STORE:
            return cls.get_store(store_type=store_type, keyfile_dict=store_access)
        return cls.get_store(store_type=store_type, **store_access)

    def set_env_vars(self):
        """Set authentication and access of the current store to the env vars"""
        pass

    @property
    def is_local_store(self):
        return self.STORE_TYPE == self._LOCAL_STORE

    @property
    def is_s3_store(self):
        return self.STORE_TYPE == self._S3_STORE

    @property
    def is_azure_store(self):
        return self.STORE_TYPE == self._AZURE_STORE

    @property
    def is_gcs_store(self):
        return self.STORE_TYPE == self._GCS_STORE

    def ls(self, path):
        raise NotImplementedError

    def list(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def download_file(self, *args, **kwargs):
        raise NotImplementedError

    def download_dir(self, *args, **kwargs):
        raise NotImplementedError

    def upload_file(self, *args, **kwargs):
        raise NotImplementedError

    def upload_dir(self, *args, **kwargs):
        raise NotImplementedError
