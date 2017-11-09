# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.response import Response

from experiments.models import (
    Experiment,
    ExperimentJob,
    ExperimentStatus,
    ExperimentJobStatus)
from experiments.serializers import (
    ExperimentSerializer,
    ExperimentDetailSerializer,
    StatusSerializer,
    ExperimentCreateSerializer,
    ExperimentStatusSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer)
from experiments.tasks import start_experiment, get_experiment_run_status
from libs.views import BaseNestingFilterMixin, ListCreateAPIView
from projects.models import Project, Polyaxonfile


class ProjectOrPolyaxonfileViewFiltersMixin(BaseNestingFilterMixin):
    """A mixin to optionally filter by project or polyaxon file uuid."""

    def filter_queryset(self, queryset):
        filters = {}
        if 'project_uuid' in self.kwargs:
            project_uuid = self.kwargs['project_uuid']
            filters['project'] = get_object_or_404(Project, uuid=project_uuid)

        if 'plxfile_uuid' in self.kwargs:
            plxfile_uuid = self.kwargs['plxfile_uuid']
            filters['polyaxonfile'] = get_object_or_404(Polyaxonfile, uuid=plxfile_uuid)
        return queryset.filter(**filters)


class ExperimentListView(ProjectOrPolyaxonfileViewFiltersMixin, ListCreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    create_serializer_class = ExperimentCreateSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user)


class ExperimentDetailView(ProjectOrPolyaxonfileViewFiltersMixin, RetrieveUpdateDestroyAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    lookup_field = 'uuid'


class ExperimentViewMixin(ProjectOrPolyaxonfileViewFiltersMixin):
    """A mixin to filter by experiment."""
    def get_experiment(self):
        experiment_uuid = self.kwargs['experiment_uuid']
        return get_object_or_404(Experiment, uuid=experiment_uuid)

    def filter_queryset(self, queryset):
        queryset = super(ExperimentViewMixin, self).filter_queryset(queryset)
        return queryset.filter(experiment=self.get_experiment())


class ExperimentStatusListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentStatusDetailView(ExperimentViewMixin, RetrieveAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    lookup_field = 'uuid'


class ExperimentJobListView(ListCreateAPIView, ExperimentViewMixin):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentJobDetailView(ExperimentViewMixin, RetrieveUpdateDestroyAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer
    lookup_field = 'uuid'


class ExperimentJobViewMixin(ProjectOrPolyaxonfileViewFiltersMixin):
    """A mixin to filter by experiment job."""
    def get_experiment_job(self):
        experiment_uuid = self.kwargs['experiment_uuid']
        experiment_job_uuid = self.kwargs['experiment_job_uuid']
        return get_object_or_404(ExperimentJob,
                                 uuid=experiment_job_uuid,
                                 experiment__uuid=experiment_uuid)

    def filter_queryset(self, queryset):
        queryset = super(ExperimentJobViewMixin, self).filter_queryset(queryset)
        return queryset.filter(job=self.get_experiment_job())


class ExperimentJobStatusListView(ListCreateAPIView, ExperimentJobViewMixin):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer

    def perform_create(self, serializer):
        serializer.save(job=self.get_experiment_job())


class ExperimentJobStatusDetailView(ExperimentJobViewMixin, RetrieveUpdateAPIView):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    lookup_field = 'uuid'


class ExperimentStartView(CreateAPIView, RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = StatusSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(get_experiment_run_status(obj))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        job_info = start_experiment(obj)
        if job_info['status'] == 'PENDING':
            return Response(status=status.HTTP_201_CREATED, data=job_info)
        return Response(job_info, status=status.HTTP_200_OK)
