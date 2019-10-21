from rest_framework.exceptions import ValidationError


class NamesMixin(object):
    def validated_name(self, validated_data, project, query):
        name = validated_data.get('name')
        if name and query.filter(project=project, name=name).exists():
            count = query.exclude(name=name).filter(name__startswith=name).count() + 1
            validated_data['name'] = '{}-{}'.format(name, count)
        return validated_data


class CatalogNamesMixin(object):

    def validated_name(self, validated_data, owner, query):
        name = validated_data.get('name')
        if name and query.filter(owner=owner, name=name).exists():
            raise ValidationError('An instance already exists with this name.')
        return validated_data
