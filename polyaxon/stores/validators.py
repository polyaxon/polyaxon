from django.conf import settings

from stores.exceptions import VolumeNotFoundError


def validate_persistence_data(persistence_data):
    # If no persistence is defined we mount all
    return persistence_data or settings.PERSISTENCE_DATA.keys()


def validate_persistence_outputs(persistence_outputs):
    # If no persistence is defined we mount the first one as default
    if not persistence_outputs:
        return list(settings.PERSISTENCE_OUTPUTS.keys())[0]
    if not isinstance(persistence_outputs, str):
        raise VolumeNotFoundError('Persistence outputs value is not valid `{}`, '
                                  'it should be a string.'.format(persistence_outputs))
    return persistence_outputs
