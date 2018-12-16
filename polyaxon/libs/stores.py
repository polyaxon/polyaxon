from polystores.stores.manager import StoreManager
from rhea import RheaError

from django.conf import settings

from constants import stores
from libs.paths.exceptions import VolumeNotFoundError
from polyaxon.config_manager import config


def get_store_secret_from_definition(volume_name, volume_settings):
    if volume_name not in volume_settings:
        raise VolumeNotFoundError('Volume with name `{}` was defined in specification, '
                                  'but was not found'.format(volume_name))

    definition = volume_settings[volume_name]
    store = definition.get('store')
    secret = definition.get('secret')
    secret_key = definition.get('secretKey')

    if store:
        if store not in stores.VALUES:
            raise VolumeNotFoundError(
                'Volume with store class `{}` is not supported.'.format(store))

        if not secret:
            raise VolumeNotFoundError(
                'Volume with store class `{}` does not define a secret.'.format(store))

        if not secret_key:
            raise VolumeNotFoundError(
                'Volume with store class `{}` does not define a secretKey.'.format(store))

    return store, secret, secret_key


def get_outputs_store(persistence_outputs):
    store, _, secret_key = get_store_secret_from_definition(
        volume_name=persistence_outputs,
        volume_settings=settings.PERSISTENCE_OUTPUTS)
    if not store or not secret_key:
        return StoreManager()
    try:
        store_access = config.get_dict(secret_key)
    except RheaError:
        raise VolumeNotFoundError(
            'Could not create store for path,'
            'received a store type `{}` without valid access key.'.format(store))

    return StoreManager.get_for_type(store_type=store, store_access=store_access)
