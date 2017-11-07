# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import fields, serializers

from clusters.models import Cluster, ClusterNode, GPU


class GPUSerilizer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = GPU
        exclude = ('id', 'cluster_node')


class ClusterNodeSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = ClusterNode
        fields = ('uuid', 'name', 'hostname', 'role', 'memory', 'n_cpus', 'n_gpus',)


class ClusterNodeDetailSerializer(ClusterNodeSerializer):
    gpus = GPUSerilizer(many=True)
    cluster = fields.SerializerMethodField()

    class Meta:
        model = ClusterNode
        exclude = ('id',)

    def get_cluster(self, obj):
        return obj.cluster.uuid.hex


class ClusterSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    user = fields.SerializerMethodField()

    class Meta:
        model = Cluster
        fields = ('uuid', 'user', 'version_api', 'created_at', 'updated_at', )

    def get_user(self, obj):
        return obj.user.username


class ClusterDetailSerializer(ClusterSerializer):
    nodes = ClusterNodeSerializer(many=True)

    class Meta:
        model = Cluster
        exclude = ('id',)

