from django.conf import settings

from libs.paths.exceptions import VolumeNotFoundError


def validate_persistence_outputs(persistence_outputs):
    # If no persistence is defined we mount the first one as default
    if not persistence_outputs:
        return list(settings.PERSISTENCE_OUTPUTS.keys())[0]
    if not isinstance(persistence_outputs, str):
        raise VolumeNotFoundError('Persistence outputs value is not valid `{}`, '
                                  'it should be a string.'.format(persistence_outputs))
    return persistence_outputs


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
