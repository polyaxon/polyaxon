# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
    CreateAPIView, ListAPIView)

from libs.views import ListCreateAPIView
from projects.models import Project, ExperimentGroup
from projects.serializers import (
    ProjectSerializer,
    ExperimentGroupSerializer,
)


class ProjectCreateView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        project = serializer.validated_data['name']
        user = self.request.user
        if self.queryset.filter(user=user, name=project).count() > 0:
            raise ValidationError('A project with name `{}` already exists.'.format(project))
        serializer.save(user=user)


class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)


class ExperimentGroupListView(ListCreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer

    def get_project(self):
        username = self.kwargs['username']
        project_name = self.kwargs['name']
        return get_object_or_404(Project, name=project_name, user__username=username)

    def filter_queryset(self, queryset):
        return queryset.filter(project=self.get_project())

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user, project=self.get_project())


class ExperimentGroupDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    lookup_field = 'uuid'
