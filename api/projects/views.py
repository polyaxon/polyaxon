# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import (
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from libs.views import ListCreateAPIView
from projects.models import Project, Polyaxonfile
from projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    PolyaxonfileSerializer,
)


class ProjectListView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user)


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'uuid'


class ProjectPolyaxonfileViewMixin(object):
    def get_project(self):
        project_uuid = self.kwargs['project_uuid']
        return get_object_or_404(Project, uuid=project_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(project=self.get_project())


class ProjectPolyaxonfileListView(ListCreateAPIView, ProjectPolyaxonfileViewMixin):
    queryset = Polyaxonfile.objects.all()
    serializer_class = PolyaxonfileSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user, project=self.get_project())


class ProjectPolyaxonfileDetailView(RetrieveDestroyAPIView, ProjectPolyaxonfileViewMixin):
    queryset = Polyaxonfile.objects.all()
    serializer_class = PolyaxonfileSerializer
    lookup_field = 'uuid'
