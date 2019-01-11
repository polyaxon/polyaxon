from rest_framework.exceptions import ValidationError

from schemas.environments import PersistenceConfig
from stores.exceptions import VolumeNotFoundError
from stores.validators import validate_persistence_data, validate_persistence_outputs


def _set_persistence(instance, default_persistence_data=None, default_persistence_outputs=None):
    if instance.persistence:
        return

    persistence_data = None
    persistence_outputs = None
    if instance.specification and instance.specification.persistence:
        persistence_data = instance.specification.persistence.data
        persistence_outputs = instance.specification.persistence.outputs
    if not persistence_data and default_persistence_data:
        persistence_data = default_persistence_data

    if not persistence_outputs and default_persistence_outputs:
        persistence_outputs = default_persistence_outputs

    persistence_data = validate_persistence_data(persistence_data=persistence_data)
    persistence_outputs = validate_persistence_outputs(persistence_outputs=persistence_outputs)
    persistence_config = PersistenceConfig(data=persistence_data, outputs=persistence_outputs)
    instance.persistence = persistence_config.to_dict()


def set_persistence(instance, default_persistence_data=None, default_persistence_outputs=None):
    try:
        _set_persistence(instance=instance,
                         default_persistence_data=default_persistence_data,
                         default_persistence_outputs=default_persistence_outputs)
    except VolumeNotFoundError as e:
        raise ValidationError(e)
