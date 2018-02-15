# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from plugins.serializers import TensorboardJobSerializer
from projects.models import Project
from projects.permissions import IsProjectOwnerOrPublicReadOnly
from projects.tasks import start_tensorboard, stop_tensorboard


class StartTensorboardView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = TensorboardJobSerializer
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    @staticmethod
    def _get_default_tensorboard_config(project):
        return {
            'config': {
                'version': 1,
                'project': {'name': project.name},
                'run': {'image': settings.TENSORBOARD_DOCKER_IMAGE}
            }
        }

    def _should_create_tensorboard_job(self, project):
        # If the project already has a tensorboard specification
        # and no data is provided to update
        # then we do not need to create a TensorboardJob
        if project.tensorboard and not self.request.data:
            return False
        return True

    def _create_tensorboard(self, project):
        if not self._should_create_tensorboard_job(project):
            return
        config = self.request.data or self._get_default_tensorboard_config(project)
        serializer = self.get_serializer(instance=project.tensorboard, data=config)
        serializer.is_valid(raise_exception=True)
        project.tensorboard = serializer.save(user=self.request.user, project=project)
        project.save()

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.has_tensorboard:
            self._create_tensorboard(obj)
            start_tensorboard.delay(project_id=obj.id)
        return Response(status=status.HTTP_200_OK)


class StopTensorboardView(CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.has_tensorboard:
            stop_tensorboard.delay(project_id=obj.id)
        return Response(status=status.HTTP_200_OK)
