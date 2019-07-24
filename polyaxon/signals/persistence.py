from hestia.list_utils import to_list
from rest_framework.exceptions import ValidationError

from schemas import PersistenceConfig
from stores.exceptions import StoreNotFoundError
from stores.validators import validate_persistence_data, validate_persistence_outputs


def _set_persistence(instance, default_persistence_data=None, default_persistence_outputs=None):
    if instance.persistence:
        return

    data_refs = None
    artifact_refs = None

    cond = (instance.specification and
            instance.specification.environment and
            instance.specification.environment.data_refs)
    if cond:
        data_refs = instance.specification.environment.data_refs

    cond = (instance.specification and
            instance.specification.environment and
            instance.specification.environment.artifact_refs)
    if cond:
        # TODO: this is a temp workaround until the finalized Polyflow version
        artifact_refs = to_list(instance.specification.environment.artifact_refs)[0]

    if not data_refs and default_persistence_data:
        data_refs = default_persistence_data

    if not artifact_refs and default_persistence_outputs:
        artifact_refs = default_persistence_outputs

    persistence_data = validate_persistence_data(persistence_data=data_refs)
    persistence_outputs = validate_persistence_outputs(persistence_outputs=artifact_refs)
    persistence_config = PersistenceConfig(data=persistence_data, outputs=persistence_outputs)
    instance.persistence = persistence_config.to_dict()


def set_persistence(instance, default_persistence_data=None, default_persistence_outputs=None):
    try:
        _set_persistence(instance=instance,
                         default_persistence_data=default_persistence_data,
                         default_persistence_outputs=default_persistence_outputs)
    except StoreNotFoundError as e:
        raise ValidationError(e)
