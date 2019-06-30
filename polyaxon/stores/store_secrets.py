from constants.store_types import StoreTypes
from stores.exceptions import StoreNotFoundError


def get_store_secret_from_definition(definition):
    store = definition.get('store')
    secret = definition.get('secret')
    secret_key = definition.get('secretKey')

    if store:
        if store not in StoreTypes.CLOUD_STORES:
            raise StoreNotFoundError(
                'Volume with store class `{}` is not supported.'.format(store))

        if not secret:
            raise StoreNotFoundError(
                'Volume with store class `{}` does not define a secret.'.format(store))

        if not secret_key:
            raise StoreNotFoundError(
                'Volume with store class `{}` does not define a secretKey.'.format(store))

    return store, secret, secret_key


def get_store_secret_for_persistence(volume_name, volume_settings):
    if volume_name not in volume_settings:
        raise StoreNotFoundError('Volume with name `{}` was defined in specification, '
                                 'but was not found'.format(volume_name))

    definition = volume_settings[volume_name]
    return get_store_secret_from_definition(definition)
