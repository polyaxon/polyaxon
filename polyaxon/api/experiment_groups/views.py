from hestia.bool_utils import to_bool
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import auditor
import conf

from api.endpoint.base import (
    BaseEndpoint,
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.endpoint.group import (
    ExperimentGroupEndpoint,
    ExperimentGroupResourceEndpoint,
    ExperimentGroupResourceListEndpoint
)
from api.endpoint.project import ProjectResourceListEndpoint
from api.experiment_groups import queries
from api.experiment_groups.serializers import (
    BookmarkedExperimentGroupSerializer,
    ExperimentGroupChartViewSerializer,
    ExperimentGroupCreateSerializer,
    ExperimentGroupDetailSerializer,
    ExperimentGroupSerializer,
    ExperimentGroupStatusSerializer
)
from api.experiments.serializers import ExperimentMetricSerializer
from api.filters import OrderingFilter, QueryFilter
from api.paginator import LargeLimitOffsetPagination
from api.utils.views.bookmarks_mixin import BookmarkedListMixinView
from db.models.experiment_groups import (
    ExperimentGroup,
    ExperimentGroupChartView,
    ExperimentGroupStatus
)
from db.models.experiments import ExperimentMetric
from event_manager.events.chart_view import CHART_VIEW_CREATED, CHART_VIEW_DELETED
from event_manager.events.experiment_group import (
    EXPERIMENT_GROUP_ARCHIVED,
    EXPERIMENT_GROUP_DELETED_TRIGGERED,
    EXPERIMENT_GROUP_METRICS_VIEWED,
    EXPERIMENT_GROUP_RESTORED,
    EXPERIMENT_GROUP_STATUSES_VIEWED,
    EXPERIMENT_GROUP_STOPPED_TRIGGERED,
    EXPERIMENT_GROUP_UPDATED,
    EXPERIMENT_GROUP_VIEWED
)
from event_manager.events.project import PROJECT_EXPERIMENT_GROUPS_VIEWED
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from scopes.permissions.projects import IsItemProjectOwnerOrPublicReadOnly, get_permissible_project


class ExperimentGroupListView(BookmarkedListMixinView,
                              ProjectResourceListEndpoint,
                              ListEndpoint,
                              CreateEndpoint):
    """
    get:
        List experiment groups under a project.

    post:
        Create an experiment group under a project.
    """
    queryset = queries.groups
    serializer_class = BookmarkedExperimentGroupSerializer
    create_serializer_class = ExperimentGroupCreateSerializer
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'experiment_group'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')

    def filter_queryset(self, queryset):
        auditor.record(event_type=PROJECT_EXPERIMENT_GROUPS_VIEWED,
                       instance=self.project,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        return super().filter_queryset(queryset=queryset)

    def perform_create(self, serializer):
        project = self.project
        instance = serializer.save(user=self.request.user,
                                   project=project)
        experiment_ids = self.request.data.get('experiment_ids')
        if instance.is_selection and experiment_ids:
            experiment_ids = set(experiment_ids)
            if len(experiment_ids) != project.experiments.filter(id__in=experiment_ids).count():
                raise ValidationError('Experiments selection is not valid.')
            instance.selection_experiments.set(experiment_ids)


class ExperimentGroupDetailView(ExperimentGroupEndpoint,
                                RetrieveEndpoint,
                                DestroyEndpoint,
                                UpdateEndpoint):
    """
    get:
        Get an experiment group details.
    patch:
        Update an experiment group details.
    delete:
        Delete an experiment group.
    """
    queryset = queries.groups_details
    serializer_class = ExperimentGroupDetailSerializer
    AUDITOR_EVENT_TYPES = {
        'GET': EXPERIMENT_GROUP_VIEWED,
        'UPDATE': EXPERIMENT_GROUP_UPDATED,
        'DELETE': EXPERIMENT_GROUP_DELETED_TRIGGERED
    }

    def perform_destroy(self, instance):
        instance.archive()
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_SCHEDULE_DELETION,
            kwargs={'experiment_group_id': instance.id, 'immediate': True},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


class ExperimentGroupArchiveView(ExperimentGroupEndpoint, CreateEndpoint):
    """Restore an experiment."""
    serializer_class = ExperimentGroupSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_GROUP_ARCHIVED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_GROUP_SCHEDULE_DELETION,
            kwargs={'experiment_group_id': obj.id, 'immediate': False},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class ExperimentGroupRestoreView(ExperimentGroupEndpoint, CreateEndpoint):
    """Restore an experiment."""
    queryset = ExperimentGroup.all
    serializer_class = ExperimentGroupSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_GROUP_RESTORED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        obj.restore()
        return Response(status=status.HTTP_200_OK)


class ExperimentGroupSelectionView(ExperimentGroupEndpoint, UpdateEndpoint):
    queryset = ExperimentGroup.objects
    serializer_class = None

    def update(self, request, *args, **kwargs):
        group = self.group
        if not group.is_selection:
            raise ValidationError('This group is a not a selection.')

        project = self.project
        op = self.request.data.get('operation')
        experiment_ids = self.request.data.get('experiment_ids')
        if experiment_ids:
            experiment_ids = set(experiment_ids)
            if len(experiment_ids) != project.experiments.filter(id__in=experiment_ids).count():
                raise ValidationError('Experiments selection is not valid.')
            if op == 'add':
                group.selection_experiments.add(*experiment_ids)
            elif op == 'remove':
                group.selection_experiments.remove(*experiment_ids)
            elif op is None:
                group.selection_experiments.set(experiment_ids)
            else:
                raise ValidationError('Received an invalid operation.')
        return Response(status=status.HTTP_200_OK)


class ExperimentGroupStopView(CreateAPIView):
    """Stop an experiment group."""
    queryset = ExperimentGroup.objects.all()
    serializer_class = ExperimentGroupSerializer
    permission_classes = (IsAuthenticated, IsItemProjectOwnerOrPublicReadOnly)
    lookup_field = 'id'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        pending = request.data.get('pending')
        pending = to_bool(pending) if pending is not None else False
        auditor.record(event_type=EXPERIMENT_GROUP_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username,
                       pending=pending)
        if pending:
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS,
                kwargs={'experiment_group_id': obj.id,
                        'pending': pending,
                        'message': 'User stopped pending experiments'},
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        else:
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP,
                kwargs={'experiment_group_id': obj.id,
                        'message': 'User stopped experiment group'},
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class ExperimentGroupViewMixin(object):
    """A mixin to filter by experiment group."""
    project = None
    group = None

    def get_experiment_group(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        group_id = self.kwargs['group_id']
        self.group = get_object_or_404(ExperimentGroup, project=self.project, id=group_id)
        return self.group

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(experiment_group=self.get_experiment_group())


class ExperimentGroupStatusListView(ExperimentGroupResourceListEndpoint,
                                    ListEndpoint,
                                    CreateEndpoint):
    """
    get:
        List all statuses of experiment group.
    post:
        Create an experiment group status.
    """
    queryset = ExperimentGroupStatus.objects.order_by('created_at').all()
    serializer_class = ExperimentGroupStatusSerializer

    def perform_create(self, serializer):
        serializer.save(experiment_group=self.group)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_GROUP_STATUSES_VIEWED,
                       instance=self.group,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentGroupMetricsListView(ExperimentGroupResourceListEndpoint, ListEndpoint):
    """
    get:
        List all metrics of experiments under a group.
    """
    queryset = ExperimentMetric.objects.all()
    serializer_class = ExperimentMetricSerializer
    pagination_class = LargeLimitOffsetPagination

    def filter_queryset(self, queryset):
        queryset = super(BaseEndpoint, self).filter_queryset(  # pylint:disable=bad-super-call
            queryset)
        if self.group.is_study:
            return queryset.filter(experiment__experiment_group=self.group)
        elif self.group.is_selection:
            return queryset.filter(experiment__selections=self.group)
        raise ValidationError('Invalid group.')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_GROUP_METRICS_VIEWED,
                       instance=self.group,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentGroupChartViewListView(ExperimentGroupResourceListEndpoint,
                                       ListEndpoint,
                                       CreateEndpoint):
    """
    get:
        List all chart views of an experiment group.
    post:
        Create an experiment group chart view.
    """
    queryset = ExperimentGroupChartView.objects.all()
    serializer_class = ExperimentGroupChartViewSerializer
    pagination_class = LargeLimitOffsetPagination

    def perform_create(self, serializer):
        instance = serializer.save(experiment_group=self.group)
        auditor.record(event_type=CHART_VIEW_CREATED,
                       instance=instance,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username,
                       group=self.group)


class ExperimentGroupChartViewDetailView(ExperimentGroupResourceEndpoint,
                                         RetrieveEndpoint,
                                         UpdateEndpoint,
                                         DestroyEndpoint):
    """
    get:
        Get experiment group chart view details.
    patch:
        Update an experiment group chart view details.
    delete:
        Delete an experiment group chart view.
    """
    queryset = ExperimentGroupChartView.objects.all()
    serializer_class = ExperimentGroupChartViewSerializer
    lookup_field = 'id'

    def get_object(self):
        if self._object:
            return self._object
        self._object = super().get_object()
        if self.request.method == 'DELETE':
            auditor.record(event_type=CHART_VIEW_DELETED,
                           instance=self._object,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           group=self._object)
        return self._object
