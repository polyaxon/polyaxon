from rest_framework import serializers

from db.models.job_resources import JobResources


class JobResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResources
        exclude = ('id',)
