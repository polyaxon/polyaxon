# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import serializers

from core.serialiazers import ExperimentSerializer
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name',)


class ProjectDetailSerializer(serializers.ModelSerializer):
    experiments = ExperimentSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'
