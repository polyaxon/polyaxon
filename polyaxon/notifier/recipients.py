from collections import namedtuple


class RecipientSpec(namedtuple('RecipientSpec', 'id email')):
    pass


def get_project_recipients(project):
    return {RecipientSpec(project.user.id, project.user.email), }


def get_build_recipients(build):
    recipients = {RecipientSpec(build.user.id, build.user.email), }
    recipients |= get_project_recipients(build.project)
    return recipients


def get_instance_and_project_recipients(instance):
    recipients = {RecipientSpec(instance.user.id, instance.user.email), }
    recipients |= get_project_recipients(instance.project)
    return recipients

