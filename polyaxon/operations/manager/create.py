from operations.manager.models import ENTITY_MODELS


def create_entity(user_id, project_id, entity_type, content):
    return ENTITY_MODELS[entity_type].objects.create(
        user_id=user_id,
        project_id=project_id,
        content=content)
