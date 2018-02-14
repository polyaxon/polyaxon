# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import serializers, fields

from libs.spec_validation import validate_tensorboard_spec_content
from plugins.models import TensorboardJob


class TensorboardJobSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        model = TensorboardJob
        fields = ('user', 'config', )

    def get_user(self, obj):
        return obj.user.username

    def validate_config(self, config):
        # content is optional
        if not config:
            return config

        validate_tensorboard_spec_content(config)

        # Resume normal creation
        return config
