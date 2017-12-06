# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from repos.models import Repo


class RepoSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()
    project = fields.SerializerMethodField()

    class Meta:
        model = Repo
        fields = ('user', 'project', 'created_at', 'updated_at', 'is_public', )

    def get_user(self, obj):
        return obj.user.username

    def get_project(self, obj):
        return obj.project.name
