# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from datasets.models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = (
            'uuid', 'user', 'name', 'version', 'description',
            'created_at', 'updated_at', 'is_public',)

    def get_user(self, obj):
        return obj.user.username
