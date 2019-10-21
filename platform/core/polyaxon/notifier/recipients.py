from collections import namedtuple
from typing import Any, Set


class RecipientSpec(namedtuple('RecipientSpec', 'id email')):
    pass


def get_project_recipients(project: 'Project') -> Set[RecipientSpec]:
    return {RecipientSpec(project.user.id, project.user.email), }


def get_build_recipients(build: 'BuildJob') -> Set[RecipientSpec]:
    recipients = {RecipientSpec(build.user.id, build.user.email), }
    recipients |= get_project_recipients(build.project)
    return recipients


def get_instance_and_project_recipients(instance: Any) -> Set[RecipientSpec]:
    recipients = {RecipientSpec(instance.user.id, instance.user.email), }
    recipients |= get_project_recipients(instance.project)
    return recipients
