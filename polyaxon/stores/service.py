from hestia.service_interface import InvalidService, Service

from marshmallow import ValidationError

from django.conf import settings
from polystores import StoreManager
from rhea import RheaError

from stores.exceptions import VolumeNotFoundError
from stores.store_secrets import get_store_secret_for_persistence, get_store_secret_from_definition
from stores.validators import validate_persistence_data, validate_persistence_outputs
from stores.schemas.store import StoreConfig
from stores.schemas.volume import VolumeConfig
from polyaxon.config_manager import config


class StoresService(Service):
    __all__ = (
        'setup',
        'get_data_paths',
        'get_logs_paths',
        'get_outputs_paths',
        'get_outputs_store',
        'get_logs_store',
    )

    @staticmethod
    def _validate_persistence(persistence, persistence_name, persistence_type):
        try:
            VolumeConfig.from_dict(persistence)
        except ValidationError:
            try:
                StoreConfig.from_dict(persistence)
            except (ValidationError, TypeError):
                raise InvalidService('Persistence `{}`, of type `{}`, is not valid.'.format(
                    persistence_name, persistence_type
                ))

    @staticmethod
    def get_data_paths(persistence_data):
        persistence_data = validate_persistence_data(persistence_data=persistence_data)
        persistence_paths = {}
        for persistence in persistence_data:
            if persistence not in settings.PERSISTENCE_DATA:
                raise VolumeNotFoundError(
                    'Data volume with name `{}` was defined in specification, '
                    'but was not found'.format(persistence))
            persistence_type_condition = (
                'mountPath' not in settings.PERSISTENCE_DATA[persistence] and
                'bucket' not in settings.PERSISTENCE_DATA[persistence]
            )
            if persistence_type_condition:
                raise VolumeNotFoundError('Data volume with name `{}` '
                                          'does not define a mountPath or bucket.'.format(
                    persistence))

            persistence_paths[persistence] = (
                    settings.PERSISTENCE_DATA[persistence].get('mountPath') or
                    settings.PERSISTENCE_DATA[persistence].get('bucket'))

        return persistence_paths

    @staticmethod
    def get_outputs_paths(persistence_outputs):
        persistence_outputs = validate_persistence_outputs(persistence_outputs=persistence_outputs)
        if persistence_outputs not in settings.PERSISTENCE_OUTPUTS:
            raise VolumeNotFoundError('Outputs volume with name `{}` was defined in specification, '
                                      'but was not found'.format(persistence_outputs))
        persistence_type_condition = (
            'mountPath' not in settings.PERSISTENCE_OUTPUTS[persistence_outputs] and
            'bucket' not in settings.PERSISTENCE_OUTPUTS[persistence_outputs]
        )
        if persistence_type_condition:
            raise VolumeNotFoundError(
                'Outputs volume with name `{}` '
                'does not define a mountPath or bucket.'.format(persistence_outputs))

        return (settings.PERSISTENCE_OUTPUTS[persistence_outputs].get('mountPath') or
                settings.PERSISTENCE_OUTPUTS[persistence_outputs].get('bucket'))

    @staticmethod
    def delete_outputs_paths(outputs_path, persistence_outputs):
        pass

    @staticmethod
    def get_logs_paths(persistence_logs='default'):
        persistence_type_condition = (
            'mountPath' not in settings.PERSISTENCE_LOGS and
            'bucket' not in settings.PERSISTENCE_LOGS
        )
        if persistence_type_condition:
            raise VolumeNotFoundError('Logs volume does not define a mountPath or bucket.')

        return settings.PERSISTENCE_LOGS.get('mountPath') or settings.PERSISTENCE_LOGS.get('bucket')

    @staticmethod
    def delete_logs_paths(outputs_path, persistence_logs='default'):
        pass

    @staticmethod
    def _get_store(store, secret_key):
        if not store or not secret_key:
            return StoreManager()
        try:
            store_access = config.get_dict(secret_key)
        except RheaError:
            raise VolumeNotFoundError(
                'Could not create store for path,'
                'received a store type `{}` without valid access key.'.format(store))

        return StoreManager.get_for_type(store_type=store, store_access=store_access)

    @classmethod
    def get_outputs_store(cls, persistence_outputs):
        store, _, secret_key = get_store_secret_for_persistence(
            volume_name=persistence_outputs,
            volume_settings=settings.PERSISTENCE_OUTPUTS)
        return cls._get_store(store, secret_key)

    @classmethod
    def get_logs_store(cls, persistence_logs='default'):
        store, _, secret_key = get_store_secret_from_definition(settings.PERSISTENCE_LOGS)
        return cls._get_store(store, secret_key)

    def validate(self):
        self._validate_persistence(persistence=settings.PERSISTENCE_LOGS,
                                   persistence_name='default',
                                   persistence_type='PERSISTENCE_LOGS')
        for persistence_name, persistence in settings.PERSISTENCE_OUTPUTS.items():
            self._validate_persistence(persistence=persistence,
                                       persistence_name=persistence_name,
                                       persistence_type='PERSISTENCE_OUTPUTS')

        for persistence_name, persistence in settings.PERSISTENCE_DATA.items():
            self._validate_persistence(persistence=persistence,
                                       persistence_name=persistence_name,
                                       persistence_type='PERSISTENCE_OUTPUTS')
