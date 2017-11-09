# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
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


class ExperimentListView(ListCreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    create_serializer_class = ExperimentCreateSerializer

    def perform_create(self, serializer):
        # TODO: update when we allow platform usage without authentication
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.serializer_class


class ExperimentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    lookup_field = 'uuid'


class ExperimentViewMixin(object):
    def get_experiment(self):
        experiment_uuid = self.kwargs['experiment_uuid']
        return get_object_or_404(Experiment, uuid=experiment_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(experiment=self.get_experiment())


class ExperimentStatusListView(ListCreateAPIView, ExperimentViewMixin):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentStatusDetailView(RetrieveAPIView, ExperimentViewMixin):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    lookup_field = 'uuid'


class ExperimentJobListView(ListCreateAPIView, ExperimentViewMixin):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentJobDetailView(RetrieveUpdateDestroyAPIView, ExperimentViewMixin):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer
    lookup_field = 'uuid'


class ExperimentJobStatusViewMixin(object):
    def get_experiment_job(self):
        experiment_uuid = self.kwargs['experiment_uuid']
        experiment_job_uuid = self.kwargs['experiment_job_uuid']
        return get_object_or_404(ExperimentJob,
                                 uuid=experiment_job_uuid,
                                 experiment__uuid=experiment_uuid)

    def filter_queryset(self, queryset):
        return queryset.filter(job=self.get_experiment_job())


class ExperimentJobStatusListView(ListCreateAPIView, ExperimentJobStatusViewMixin):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer

    def perform_create(self, serializer):
        serializer.save(job=self.get_experiment_job())


class ExperimentJobStatusDetailView(RetrieveUpdateAPIView, ExperimentJobStatusViewMixin):
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
