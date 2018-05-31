import json

from rest_framework import fields


from api.experiments.serializers import ExperimentJobDetailSerializer


def get_job_definition(definition):
    serializer = ExperimentJobDetailSerializer(data={
        'definition': json.dumps(definition, default=fields.DateTimeField().to_representation)
    })
    serializer.is_valid()
    return json.loads(serializer.validated_data['definition'])
