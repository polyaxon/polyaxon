# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
    ListAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentStatus,
    ExperimentJobStatus)
from experiments.serializers import (
    ExperimentSerializer,
    ExperimentCreateSerializer,
    ExperimentStatusSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer)
from experiments.tasks import stop_experiment
from libs.views import ListCreateAPIView
from projects.models import ExperimentGroup
from projects.permissions import check_access_project_item, get_permissible_project, \
    IsItemProjectOwnerOrPublicReadOnly


class ExperimentListView(ListAPIView):
    """List all experiments"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)


class ProjectExperimentListView(ListCreateAPIView):
    """List/Create an experiment under a project"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    create_serializer_class = ExperimentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project=get_permissible_project(view=self))


class GroupExperimentListView(ListAPIView):
    """List all experiments under a group"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)

    def get_group(self):
        group_uuid = self.kwargs['uuid']
        group = get_object_or_404(ExperimentGroup, uuid=group_uuid)

        # Check project permissions
        check_access_project_item(view=self, request=self.request, project=group.project)

        return group

    def filter_queryset(self, queryset):
        return queryset.filter(experiment_group=self.get_group())


class ExperimentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'uuid'


class ExperimentRestartView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'uuid'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        new_obj = Experiment.objects.create(
            project=obj.project,
            user=self.request.user,
            description=obj.description,
            experiment_group=obj.experiment_group,
            config=obj.config,
            original_experiment=obj
        )
        serializer = self.get_serializer(new_obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class ExperimentStopView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'uuid'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        stop_experiment.delay(experiment_id=obj.id)
        return Response(status=status.HTTP_200_OK)


class ExperimentViewMixin(object):
    """A mixin to filter by experiment."""

    def get_experiment(self):
        experiment_uuid = self.kwargs['experiment_uuid']
        experiment = get_object_or_404(Experiment, uuid=experiment_uuid)

        # Check project permissions
        check_access_project_item(view=self, request=self.request, project=experiment.project)

        return experiment

    def filter_queryset(self, queryset):
        queryset = super(ExperimentViewMixin, self).filter_queryset(queryset)
        return queryset.filter(experiment=self.get_experiment())


class ExperimentStatusListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentStatusDetailView(ExperimentViewMixin, RetrieveAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentJobListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentJobDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'

    def get_object(self):
        obj = super(ExperimentJobDetailView, self).get_object()

        # Check project permissions
        check_access_project_item(view=self, request=self.request, project=obj.experiment.project)

        return obj


class ExperimentJobViewMixin(object):
    """A mixin to filter by experiment job."""

    def get_job(self):
        job_uuid = self.kwargs['job_uuid']
        job = get_object_or_404(ExperimentJob, uuid=job_uuid)

        # Check project permissions
        check_access_project_item(view=self, request=self.request, project=job.experiment.project)

        return job

    def filter_queryset(self, queryset):
        queryset = super(ExperimentJobViewMixin, self).filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class ExperimentJobStatusListView(ListCreateAPIView, ExperimentJobViewMixin):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(job=self.get_job())


class ExperimentJobStatusDetailView(ExperimentJobViewMixin, RetrieveUpdateAPIView):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'
