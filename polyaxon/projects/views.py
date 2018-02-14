# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from libs.views import ListCreateAPIView
from plugins.serializers import TensorboardJobSerializer
from projects.models import Project, ExperimentGroup
from projects.permissions import (
    IsProjectOwnerOrPublicReadOnly,
    get_permissible_project,
    IsItemProjectOwnerOrPublicReadOnly)
from projects.serializers import (
    ProjectSerializer,
    ExperimentGroupSerializer,
    ExperimentGroupDetailSerializer,
    ProjectDetailSerializer,
)
from projects.tasks import start_tensorboard, stop_tensorboard


class ProjectCreateView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        project = serializer.validated_data['name']
        user = self.request.user
        if self.queryset.filter(user=user, name=project).count() > 0:
            raise ValidationError('A project with name `{}` already exists.'.format(project))
        serializer.save(user=user)


class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        if self.request.user.is_staff or self.request.user.username == username:
            # User checking own projects
            return queryset.filter(user__username=username)
        else:
            # Use checking other user public projects
            return queryset.filter(user__username=username, is_public=True)


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)


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


class ExperimentGroupListView(ListCreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    create_serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project=get_permissible_project(view=self))


class ExperimentGroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def get_object(self):
        obj = super(ExperimentGroupDetailView, self).get_object()
        # Check project permissions
        self.check_object_permissions(self.request, obj)
        return obj
