from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

import auditor

from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_STOPPED_TRIGGERED,
    EXPERIMENT_GROUP_DELETED_TRIGGERED,
    EXPERIMENT_GROUP_UPDATED,
    EXPERIMENT_GROUP_VIEWED
)
from event_manager.events.project import PROJECT_EXPERIMENT_GROUPS_VIEWED
from db.models.experiment_groups import ExperimentGroup
from apis.experiment_groups.serializers import ExperimentGroupDetailSerializer, ExperimentGroupSerializer
from libs.utils import to_bool
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import RunnerCeleryTasks
from libs.views import AuditorMixinView, ListCreateAPIView
from permissions.projects import IsItemProjectOwnerOrPublicReadOnly, get_permissible_project


class ExperimentGroupListView(ListCreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    create_serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        project = get_permissible_project(view=self)
        auditor.record(event_type=PROJECT_EXPERIMENT_GROUPS_VIEWED,
                       instance=project,
                       actor_id=self.request.user.id)
        return queryset.filter(project=project)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project=get_permissible_project(view=self))


class ExperimentGroupDetailView(AuditorMixinView, RetrieveUpdateDestroyAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupDetailSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'sequence'
    get_event = EXPERIMENT_GROUP_VIEWED
    update_event = EXPERIMENT_GROUP_UPDATED
    delete_event = EXPERIMENT_GROUP_DELETED_TRIGGERED

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def get_object(self):
        obj = super(ExperimentGroupDetailView, self).get_object()
        # Check project permissions
        self.check_object_permissions(self.request, obj)
        return obj


class ExperimentGroupStopView(CreateAPIView):
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        pending = request.data.get('pending')
        pending = to_bool(pending) if pending is not None else False
        auditor.record(event_type=EXPERIMENT_GROUP_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id,
                       pending=pending)
        celery_app.send_task(
            RunnerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS,
            kwargs={'experiment_group_id': obj.id,
                    'pending': pending,
                    'message': 'User stopped experiment group'})
        return Response(status=status.HTTP_200_OK)
