from django.conf import settings

from libs.paths.exceptions import VolumeNotFoundError


def validate_persistence_data(persistence_data):
    # If no persistence is defined we mount all
    return persistence_data or settings.PERSISTENCE_DATA.keys()


def get_data_paths(persistence_data):
    persistence_data = validate_persistence_data(persistence_data=persistence_data)
    persistence_paths = {}
    for persistence in persistence_data:
        if persistence not in settings.PERSISTENCE_DATA:
            raise VolumeNotFoundError('Data volume with name `{}` was defined in specification, '
                                      'but was not found'.format(persistence))
        if 'mountPath' not in settings.PERSISTENCE_DATA[persistence]:
            raise VolumeNotFoundError('Data volume with name `{}` '
                                      'does not define a mountPath.'.format(persistence))

        persistence_paths[persistence] = settings.PERSISTENCE_DATA[persistence]['mountPath']

    return persistence_paths
