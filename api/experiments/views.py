# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from experiments.models import Experiment
from experiments.serializers import (
    ExperimentSerializer,
    ExperimentDetailSerializer,
    StatusSerializer)
from experiments.tasks import start_experiment, get_experiment_run_status


class ExperimentListView(ListAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ExperimentDetailView(RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
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
