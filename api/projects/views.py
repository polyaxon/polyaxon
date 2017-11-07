# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, get_object_or_404

from projects.models import Project, Polyaxonfile
from projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    PolyaxonfileSerializer)


class ProjectListView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'uuid'


class ProjectPolyaxonfileViewMixin(object):
    def get_project(self):
        project_uuid = self.kwargs['project_uuid']
        return get_object_or_404(Project, uuid=project_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(movie=self.get_project())


class ProjectPolyaxonfileListView(ListCreateAPIView, ProjectPolyaxonfileViewMixin):
    queryset = Polyaxonfile.objects.all()
    serializer_class = PolyaxonfileSerializer


class ProjectPolyaxonfileDetailView(RetrieveAPIView, ProjectPolyaxonfileViewMixin):
    queryset = Polyaxonfile.objects.all()
    serializer_class = PolyaxonfileSerializer
    lookup_field = 'uuid'
