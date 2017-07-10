# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework.generics import ListAPIView, RetrieveAPIView

from core.models import Experiment, PolyaxonModel, Estimator
from core.serialiazers import (
    ExperimentSerializer,
    ExperimentDetailSerializer,
    PolyaxonModelSerializer,
    PolyaxonModelDetailSerializer,
    EstimatorSerializer,
    EstimatorDetailSerializer)


class ExperimentListView(ListAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ExperimentDetailView(RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer


class ExperimentEstimatorDetailView(RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = EstimatorDetailSerializer

    def get_object(self):
        obj = super(ExperimentEstimatorDetailView, self).get_object()
        return obj.estimator


class ExperimentModelDetailView(RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = PolyaxonModelDetailSerializer

    def get_object(self):
        obj = super(ExperimentModelDetailView, self).get_object()
        return obj.model


class EstimatorListView(ListAPIView):
    queryset = Estimator.objects.all()
    serializer_class = EstimatorSerializer


class EstimatorDetailView(RetrieveAPIView):
    queryset = Estimator.objects.all()
    serializer_class = EstimatorDetailSerializer


class PolyaxonModelListView(ListAPIView):
    queryset = PolyaxonModel.objects.all()
    serializer_class = PolyaxonModelSerializer


class PolyaxonModelDetailView(RetrieveAPIView):
    queryset = PolyaxonModel.objects.all()
    serializer_class = PolyaxonModelDetailSerializer
