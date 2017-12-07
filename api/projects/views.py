# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from django.contrib.auth.models import User

from rest_framework.generics import (
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from libs.views import ListCreateAPIView
from projects.models import Project, PolyaxonSpec
from projects.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    PolyaxonSpecSerializer,
)


class ProjectListView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        user, _ = User.objects.get_or_create(username='owner',
                                             email='onwer@polyaxon.com',
                                             password='glass onion')
        serializer.save(user=user)


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    lookup_field = 'uuid'


class ProjectSpecViewMixin(object):
    def get_project(self):
        project_uuid = self.kwargs['project_uuid']
        return get_object_or_404(Project, uuid=project_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(project=self.get_project())


class ProjectSpecListView(ProjectSpecViewMixin, ListCreateAPIView):
    queryset = PolyaxonSpec.objects.all()
    serializer_class = PolyaxonSpecSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user, project=self.get_project())


class ProjectSpecDetailView(ProjectSpecViewMixin, RetrieveDestroyAPIView):
    queryset = PolyaxonSpec.objects.all()
    serializer_class = PolyaxonSpecSerializer
    lookup_field = 'uuid'
