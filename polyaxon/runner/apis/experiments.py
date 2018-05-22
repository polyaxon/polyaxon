from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import auditor

from event_manager.events.experiment import EXPERIMENT_STOPPED_TRIGGERED
from models.experiments import Experiment
from experiments.serializers import ExperimentSerializer
from projects.permissions import get_permissible_project
from runner.tasks.experiments import stop_experiment


class ExperimentStopView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id)
        stop_experiment.delay(experiment_id=obj.id)
        return Response(status=status.HTTP_200_OK)
