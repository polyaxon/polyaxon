from django.core.exceptions import ValidationError


def validate_resource(resource):
    """Validates a resource"""
    if resource is not None and not isinstance(resource, dict):
        raise ValidationError('The resource is not valid.')

    if isinstance(resource, dict) and set(resource.keys()) <= {'requests', 'limits'}:
        raise ValidationError(
            'The keys `{}` for the resource are not valid.'.format(set(resource.keys())))
