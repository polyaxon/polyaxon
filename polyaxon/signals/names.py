from rest_framework.exceptions import ValidationError


def set_name(instance, query):
    if instance.name and query.filter(project=instance.project, name=instance.name):
        raise ValidationError('An instance with name `{}` already exists in this project.'.format(
            instance.name
        ))
