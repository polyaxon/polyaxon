class NamesMixin(object):
    def validated_name(self, validated_data, query):
        name = validated_data.get('name')
        if name and query.filter(project=validated_data['project'], name=name).exists():
            count = query.exclude(name=name).filter(name__startswith=name).count() + 1
            validated_data['name'] = '{}-{}'.format(name, count)
        return validated_data
