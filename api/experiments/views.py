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
    ExperimentCreateSerializer,
    ExperimentStatusSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer)
from libs.views import BaseNestingFilterMixin, ListCreateAPIView
from projects.models import Project, ExperimentGroup


class ProjectOrSpecViewFiltersMixin(BaseNestingFilterMixin):
    """A mixin to optionally filter by project or polyaxon file uuid."""

    def filter_queryset(self, queryset):
        filters = {}
        if 'project_uuid' in self.kwargs:
            project_uuid = self.kwargs['project_uuid']
            filters['project'] = get_object_or_404(Project, uuid=project_uuid)

        if 'experiment_group_uuid' in self.kwargs:
            experiment_group_uuid = self.kwargs['experiment_group_uuid']
            filters['experiment_group'] = get_object_or_404(ExperimentGroup,
                                                            uuid=experiment_group_uuid)
        return queryset.filter(**filters)


class ExperimentListView(ProjectOrSpecViewFiltersMixin, ListCreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    create_serializer_class = ExperimentCreateSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user)


class ExperimentDetailView(ProjectOrSpecViewFiltersMixin, RetrieveUpdateDestroyAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    lookup_field = 'uuid'


class ExperimentViewMixin(ProjectOrSpecViewFiltersMixin):
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


class ExperimentJobViewMixin(ProjectOrSpecViewFiltersMixin):
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


class ExperimentRestartView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    lookup_field = 'uuid'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        new_obj = Experiment.objects.create(
            cluster=obj.cluster,
            project=obj.project,
            user=self.request.user,
            name=obj.name,
            description=obj.description,
            experiment_group=obj.experiment_group,
            config=obj.config,
            original_experiment=obj
        )
        serializer = self.get_serializer(new_obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
