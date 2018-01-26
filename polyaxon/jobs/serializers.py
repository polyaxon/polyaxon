# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import serializers

from jobs.models import JobResources


class JobResourcesSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobResources
        exclude = ('id',)
