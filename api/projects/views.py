# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.http import Http404
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from libs.views import ListCreateAPIView
from projects.models import Project, ExperimentGroup
from projects.serializers import (
    ProjectSerializer,
    ExperimentGroupSerializer,
)


class ProjectListView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user)


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'uuid'

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)


class ProjectDetailByNameView(ProjectDetailView):
    lookup_field = 'name'


class ExperimentGroupListView(ListCreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer

    def get_project(self):
        project_uuid = self.kwargs['uuid']
        return get_object_or_404(Project, uuid=project_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(project=self.get_project())

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user, project=self.get_project())


class ExperimentGroupDetailView(RetrieveDestroyAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    lookup_field = 'uuid'
